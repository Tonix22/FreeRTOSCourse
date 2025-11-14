# app.py
import os
import json
import random
import datetime
import time
from pathlib import Path
from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
from flask_session import Session

app = Flask(__name__)
app.secret_key = "REPLACE_ME_WITH_A_RANDOM_SECRET_KEY"
app.config["SESSION_TYPE"] = "filesystem"  # server-side sessions
Session(app)

# ---- Config ----
QUIZ_FILES = [f"Sesion{i}.json" for i in range(1, 4)]  # Sesion1.json ... Sesion7.json
QUESTIONS_PER_SECTION = 13
SECONDS_PER_QUESTION = 10  # 20 seconds per question
SUBMISSIONS_DIR = Path("submissions")
SUBMISSIONS_DIR.mkdir(exist_ok=True)

CODING_PROMPT = """

New coding feature now you can press tab!!!
You are on a tiny spaceship (ESP32) running FreeRTOS. There are two crew
tasks: Task1 and Task2. Both share:

  • One Emergency Meeting button (BTN)
  • One status LED (SHARED_GPIO)

To avoid chaos, ONLY ONE task may use SHARED_GPIO at a time, protected
by a BINARY SEMAPHORE.

Behavior:
- Both tasks periodically check the SAME BTN.
- When the button is pressed, the current task:
    1) Takes the binary semaphore (block if needed),
    2) Toggles SHARED_GPIO to signal an emergency meeting,
    3) Sends a message to the other task via a FreeRTOS queue:
           "Hello world from Task N (I think you are sus)"
    4) Gives the semaphore back.
- Each task also waits on the queue and prints any received message.

Requirements:
- Create: xGpioSem (binary semaphore), xMsgQueue (queue), Task1, Task2.
- Use xTaskCreate, xSemaphoreTake/Give, xQueueSend/Receive, vTaskDelay.
- No busy-waiting; use blocking calls when possible.

Write a compact C example showing initialization and task logic.
"""

# ---- HTML Templates (inline) ----
TPL_LOGIN = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Login - Big Quiz</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 2rem; }
    form { max-width: 480px; margin: auto; display: grid; gap: 0.8rem; }
    input, button { padding: 0.6rem 0.8rem; font-size: 1rem; }
    button { cursor: pointer; }
  </style>
</head>
<body>
  <h1>Login</h1>
  <form method="post" action="{{ url_for('start_quiz') }}">
    <label>Full name
      <input required name="full_name" placeholder="Your Name">
    </label>
    <label>Student ID
      <input required name="student_id" placeholder="ID (e.g., A0123456)">
    </label>
    <label>Email
      <input required name="email" type="email" placeholder="email@example.com">
    </label>
    <button type="submit">Start Quiz</button>
  </form>
</body>
</html>
"""

TPL_QUIZ = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Big Quiz</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 1rem; }
    .header { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid #ddd; padding-bottom: 0.5rem; margin-bottom: 1rem; }
    .section { border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }
    .q { margin: 0.8rem 0; padding: 0.8rem; border-radius: 6px; background: #f9f9f9; }
    .q h4 { margin: 0 0 0.6rem 0; }
    .options { margin-left: 1rem; }
    .options label { display: block; margin: 0.3rem 0; }
    .submit { position: sticky; bottom: 0; background: #fff; padding: 1rem 0; border-top: 1px solid #ddd; }
    .student { font-size: 0.95rem; color: #444; }
    .badge { padding: 0.25rem 0.5rem; border-radius: 0.35rem; background: #eef; display: inline-block; margin-left: 0.5rem; }
    details summary { cursor: pointer; font-weight: 600; }

    /* floating timer box with phases */
    .timer { position: fixed; top: 12px; right: 12px; z-index: 9999; min-width: 300px;
             border: 2px solid #cbd5e1; border-radius: 10px; padding: 10px 12px;
             box-shadow: 0 8px 18px rgba(0,0,0,.12); background: #f8fafc; font-size: 0.95rem; }
    .timer h3 { margin: 0 0 6px 0; font-size: 1rem; }
    .count { font-weight: 700; }
    .phase-green  { background: #ecfdf5; border-color: #10b981; }
    .phase-yellow { background: #fffbeb; border-color: #f59e0b; }
    .phase-red    { background: #fef2f2; border-color: #ef4444; }
    .seg { display:flex; gap:6px; margin-top:6px; }
    .seg div { flex:1; height:8px; border-radius:4px; background:#e5e7eb; }
    .seg .g { background:#10b981; } .seg .y { background:#f59e0b; } .seg .r { background:#ef4444; }

    /* dark code box (for the single open-ended question) */
    .code-wrap { margin-top: 10px; }
    .code-label { font-weight: 700; margin: 6px 0; }
    .code-box {
      width: 100%; min-height: 220px; resize: vertical;
      background: #0b1220; color: #e6edf3; border: 1px solid #263042; border-radius: 8px;
      padding: 10px 12px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
      font-size: 0.95rem; line-height: 1.35;
    }
    .hint { color: #64748b; font-size: .9rem; margin: 4px 0 0; }
    .prompt {
      background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px; margin-bottom: 10px;
      white-space: pre-wrap;
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>Big Quiz <span class="badge">{{ total_questions }} questions total</span></h1>
    <div class="student">
      {{ student.full_name }} &middot; {{ student.student_id }} &middot; {{ student.email }}
    </div>
  </div>

  <!-- Floating timer -->
  <div id="timerBox" class="timer">
    <h3>Time limit</h3>
    <div>
      You have <strong>{{ total_minutes }} minutes {{ total_secs }} seconds</strong> to complete the test.
      <br>There are <strong>10 seconds</strong> for each question and 10 mins for open ended question.
      <br><span>Remaining:</span> <span id="countdown" class="count"></span>
    </div>
    <div class="seg" aria-hidden="true" title="Three phases: green → yellow → red">
      <div class="g"></div><div class="y"></div><div class="r"></div>
    </div>
  </div>

  <form id="quiz-form" method="post" action="{{ url_for('submit_quiz') }}">
  {% for section in sections %}
    <div class="section">
      <details open>
        <summary>{{ section.title }}</summary>
        {% for q in section.questions %}
          <div class="q">
            <h4>{{ q.question }}</h4>
            <div class="options">
              {% if q.type == 'multiple_choice' %}
                {% for opt in q.options %}
                  <label>
                    <input type="checkbox" name="{{ q.fieldname }}" value="{{ opt }}">
                    {{ opt }}
                  </label>
                {% endfor %}
              {% elif q.type == 'true_false' %}
                <label><input type="radio" name="{{ q.fieldname }}" value="True"> True</label>
                <label><input type="radio" name="{{ q.fieldname }}" value="False"> False</label>
              {% endif %}
            </div>
          </div>
        {% endfor %}
      </details>
    </div>
  {% endfor %}

    <!-- FINAL open-ended coding question (single, last) -->
    <div class="section">
      <details open>
        <summary>Open-ended coding question (C)</summary>
        <div class="q">
          <div class="prompt">
            <strong>Prompt:</strong><br><br>{{ coding_prompt }}
          </div>
          <div class="code-wrap">
            <div class="code-label">Your C answer:</div>
            <textarea class="code-box" name="open_code"
                      placeholder="/* Implement uint32_t sar_convert_once(void) per the prompt. */"></textarea>
            <div class="hint">This answer will be saved to a separate .c file under your ID/name and also recorded in the JSON details.</div>
          </div>
        </div>
      </details>
    </div>

    <div class="submit">
      <button type="submit">Submit Quiz</button>
    </div>
  </form>

  <script>
    // Remaining seconds from server (authoritative)
    let remaining = {{ remaining_seconds }};
    const total = {{ total_quiz_seconds }};
    const countdownEl = document.getElementById('countdown');
    const form = document.getElementById('quiz-form');
    const box  = document.getElementById('timerBox');

    const t1 = total / 3;
    const t2 = (2 * total) / 3;

    function setPhase() {
      box.classList.remove('phase-green','phase-yellow','phase-red');
      if (remaining > t2) {
        box.classList.add('phase-green');
      } else if (remaining > t1) {
        box.classList.add('phase-yellow');
      } else {
        box.classList.add('phase-red');
      }
    }

    function render() {
      const m = Math.floor(remaining / 60);
      const s = Math.floor(remaining % 60);
      countdownEl.textContent = m + "m " + (s < 10 ? "0" + s : s) + "s";
      setPhase();
    }

    render();
    const timer = setInterval(() => {
      remaining -= 1;
      if (remaining <= 0) {
        clearInterval(timer);
        form.submit();   // auto-submit when time is up
        return;
      }
      render();
    }, 1000);
  </script>
  
  <script>
    document.addEventListener('DOMContentLoaded', function () {
      const box = document.querySelector('textarea.code-box');
      if (!box) return;

      box.addEventListener('keydown', function (e) {
        if (e.key === 'Tab') {
          e.preventDefault();

          const start = this.selectionStart;
          const end = this.selectionEnd;

          const tab = "\t";
          this.value =
            this.value.substring(0, start) +
            tab +
            this.value.substring(end);

          this.selectionStart = this.selectionEnd = start + tab.length;
        }
      });
    });
  </script>
  
</body>
</html>
"""


TPL_RESULT = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Results</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; margin: 2rem; }
    .card { border: 1px solid #ddd; border-radius: 8px; padding: 1rem; max-width: 720px; }
    .big { font-size: 1.2rem; }
    .muted { color: #666; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }
    a { text-decoration: none; }
  </style>
</head>
<body>
  <h1>Your Result</h1>
  <div class="card">
    <p class="big"><strong>Total correct:</strong> {{ total_correct }} / {{ total_questions }}</p>
    <p class="big"><strong>Grade (0–100):</strong> {{ grade_0_100 }}</p>
    <p class="muted">Submission ID: <span class="mono">{{ submission_id }}</span></p>
    <p>Saved files:</p>
    <ul>
      <li><span class="mono">{{ grades_path }}</span></li>
      <li><span class="mono">{{ details_path }}</span></li>
      <li><span class="mono">{{ code_path }}</span></li>
    </ul>
    <p><a href="{{ url_for('login') }}">Back to login</a></p>
  </div>
</body>
</html>
"""

# ---- Helpers ----
def load_quiz_files():
    quizzes = []
    for path in QUIZ_FILES:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        title = data.get("quiz_title") or Path(path).stem
        questions = data.get("questions", [])
        quizzes.append({"title": title, "questions": questions})
    return quizzes

def normalize_question(q):
    qtype = q.get("type", "multiple_choice")
    text = q.get("question", "").strip()
    if qtype == "true_false":
        correct_bool = bool(q.get("correct_answer"))
        options = ["True", "False"]
        random.shuffle(options)
        correct_ans = "True" if correct_bool else "False"
        return {
            "type": "true_false",
            "question": text,
            "options": options,
            "correct": [correct_ans]
        }
    else:
        opts = list(q.get("options", []))
        corr = list(q.get("correct_answers", []))
        random.shuffle(opts)
        return {
            "type": "multiple_choice",
            "question": text,
            "options": opts,
            "correct": corr
        }

def pick_10_per_section(quizzes):
    sections = []
    for qz in quizzes:
        qs = list(qz["questions"])
        random.shuffle(qs)
        take = min(QUESTIONS_PER_SECTION, len(qs))
        chosen = qs[:take]
        norm = [normalize_question(q) for q in chosen]
        sections.append({"title": qz["title"], "questions": norm})
    random.shuffle(sections)
    return sections

# ---- Routes ----
@app.get("/")
def login():
    return render_template_string(TPL_LOGIN)

@app.post("/start")
def start_quiz():
    student = {
        "full_name": request.form.get("full_name", "").strip(),
        "student_id": request.form.get("student_id", "").strip(),
        "email": request.form.get("email", "").strip()
    }
    if not all(student.values()):
        return "Missing student info", 400

    quizzes = load_quiz_files()
    sections = pick_10_per_section(quizzes)

    # Build grading (server-side authoritative answers)
    grading = []
    for sec in sections:
        gsec = {"title": sec["title"], "questions": []}
        for q in sec["questions"]:
            gsec["questions"].append({
                "type": q["type"],
                "question": q["question"],
                "correct": list(q["correct"])
            })
        grading.append(gsec)

    # Compute time limit
    total_questions = sum(len(sec["questions"]) for sec in sections)
    total_seconds = total_questions * SECONDS_PER_QUESTION + 10*60
    deadline_ts = time.time() + total_seconds   # epoch seconds

    session["student"] = student
    session["sections"] = sections
    session["grading"] = grading
    session["deadline_ts"] = deadline_ts
    session["total_questions"] = total_questions
    session.modified = True

    return redirect(url_for("quiz"))

@app.get("/quiz")
def quiz():
    student = session.get("student")
    sections = session.get("sections")
    deadline_ts = session.get("deadline_ts")
    total_questions = session.get("total_questions", 0)

    if not (student and sections and deadline_ts):
        return redirect(url_for("login"))

    # Stamp stable field names (so template posts consistent names)
    for s_idx, sec in enumerate(sections):
        for q_idx, q in enumerate(sec["questions"]):
            q["fieldname"] = f"q_{s_idx}_{q_idx}"

    # Remaining time (server authoritative)
    now = time.time()
    remaining_seconds = max(0, int(round(deadline_ts - now)))

    total_quiz_seconds = total_questions * SECONDS_PER_QUESTION + 10*60
    total_minutes, total_secs = divmod(total_quiz_seconds, 60)

    if remaining_seconds <= 0:
        # Time is up: go to submit; /submit accepts GET and POST
        return redirect(url_for("submit_quiz"))

    return render_template_string(
        TPL_QUIZ,
        student=student,
        sections=sections,
        remaining_seconds=remaining_seconds,
        total_questions=total_questions,
        total_quiz_seconds=total_quiz_seconds,
        total_minutes=total_minutes,
        total_secs=total_secs,
        coding_prompt=CODING_PROMPT
    )

@app.route("/submit", methods=["GET", "POST"])
def submit_quiz():
    code_snippets = []  # will hold at most one entry now

    student = session.get("student")
    sections = session.get("sections")
    grading = session.get("grading")
    deadline_ts = session.get("deadline_ts")

    if not (student and sections and grading and deadline_ts):
        return redirect(url_for("login"))

    # Enforce deadline (server-authoritative)
    now = time.time()
    late = now > float(deadline_ts)

    total_correct = 0
    total_questions = sum(len(sec["questions"]) for sec in sections)

    details = {
        "student": student,
        "submitted_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "late": late,
        "seconds_per_question": SECONDS_PER_QUESTION,
        "sections": []
    }

    # Grade answers (no code here per-question anymore)
    for s_idx, (sec, gsec) in enumerate(zip(sections, grading)):
        sec_detail = {"title": sec["title"], "questions": []}
        for q_idx, (q, gq) in enumerate(zip(sec["questions"], gsec["questions"])):
            field = f"q_{s_idx}_{q_idx}"

            if q["type"] == "multiple_choice":
                user_ans = request.form.getlist(field) if request.method == "POST" else []
                user_ans = [a.strip() for a in user_ans if a is not None]
                correct_set = set(a.strip() for a in gq["correct"])
                is_correct = set(user_ans) == correct_set
                if is_correct:
                    total_correct += 1

                sec_detail["questions"].append({
                    "type": "multiple_choice",
                    "question": q["question"],
                    "options_shown": q["options"],
                    "user_answers": user_ans,
                    "correct_answers": list(correct_set),
                    "is_correct": is_correct
                })

            else:
                user_ans = ""
                if request.method == "POST":
                    user_ans = request.form.get(field, "") or ""
                user_ans = user_ans.strip()
                correct_set = set(a.strip() for a in gq["correct"])
                is_correct = user_ans in correct_set
                if is_correct:
                    total_correct += 1

                sec_detail["questions"].append({
                    "type": "true_false",
                    "question": q["question"],
                    "options_shown": q["options"],
                    "user_answer": user_ans if user_ans else None,
                    "correct_answer": list(correct_set)[0] if correct_set else None,
                    "is_correct": is_correct
                })

        details["sections"].append(sec_detail)

    # Capture the single open-ended answer (last question)
    open_code = ""
    if request.method == "POST":
        open_code = request.form.get("open_code", "") or ""
    open_code = open_code.rstrip()

    details["open_ended"] = {
        "prompt": CODING_PROMPT,
        "code": open_code if open_code else None
    }

    # Final grade (0..100)
    grade_0_100 = round((total_correct / total_questions) * 100, 2) if total_questions else 0.0

    # Filenames
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = f"{student['student_id']}_{ts}".replace(" ", "_")

    # Aggregated code file (only the open-ended now)
    safe_fullname = "".join(ch if ch.isalnum() or ch in ("_", "-") else "_" for ch in student["full_name"])
    code_filename = f"{student['student_id']}_{safe_fullname}.c"
    code_path = SUBMISSIONS_DIR / code_filename

    if open_code:
        with open(code_path, "w", encoding="utf-8") as cf:
            cf.write(
                f"/* Student: {student['full_name']} ({student['student_id']})  Email: {student['email']}\n"
                f"   Submitted: {details['submitted_at']}  Late: {details['late']}\n"
                f"   Open-ended coding question (C) */\n\n"
            )
            cf.write("/* ===== Prompt ===== */\n")
            cf.write(CODING_PROMPT + "\n\n")
            cf.write("/* ===== Answer ===== */\n")
            cf.write(open_code + "\n")
    else:
        # Optional: create an empty file
        # open(code_path, "w", encoding="utf-8").close()
        pass

    # Include code file path in JSONs
    details["code_file"] = str(code_path) if open_code else None

    grades_doc = {
        "student": student,
        "submitted_at": details["submitted_at"],
        "total_questions": total_questions,
        "total_correct": total_correct,
        "grade_0_100": grade_0_100,
        "late": late,
        "code_file": str(code_path) if open_code else None
    }

    # Save JSONs
    grades_path = SUBMISSIONS_DIR / f"{safe_name}_grades.json"
    with open(grades_path, "w", encoding="utf-8") as f:
        json.dump(grades_doc, f, ensure_ascii=False, indent=2)

    details_path = SUBMISSIONS_DIR / f"{safe_name}_details.json"
    with open(details_path, "w", encoding="utf-8") as f:
        json.dump(details, f, ensure_ascii=False, indent=2)

    # Clear quiz data from session
    for k in ("sections", "grading", "deadline_ts", "total_questions"):
        session.pop(k, None)

    return render_template_string(
        TPL_RESULT,
        total_correct=total_correct,
        total_questions=total_questions,
        grade_0_100=grade_0_100,
        submission_id=safe_name,
        grades_path=str(grades_path),
        details_path=str(details_path),
        code_path=str(code_path) if open_code else "N/A"
    )

# Convenience: JSON API to check health
@app.get("/healthz")
def healthz():
    return jsonify({"ok": True})

if __name__ == "__main__":
    # Run: python app.py
    # Then visit: http://127.0.0.1:5000/
    app.run(host="0.0.0.0", port=5000, debug=True)
