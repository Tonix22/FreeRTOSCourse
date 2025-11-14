import sys
import json
from bs4 import BeautifulSoup


def extract_questions(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    questions = []

    # All question cards
    qcards = soup.find_all("div", attrs={"data-functional-selector": "question-card"})
    qid = 1

    for card in qcards:
        # ---------- Question text ----------
        q_text_span = card.select_one("span.styles__Question-sc-285g7y-5")
        if q_text_span:
            q_text = q_text_span.get_text(strip=True)
        else:
            q_text = f"Question {qid}"

        # ---------- Choices ----------
        options = []
        correct_answers = []

        # Each choice row
        for choice_div in card.select("div.styles__Choice-sc-285g7y-7"):
            # Text of the option
            text_span = choice_div.select_one("span.styles__Text-sc-285g7y-11")
            if not text_span:
                continue
            opt_text = text_span.get_text(strip=True)

            # Status icon: aria-hidden="false" and data-functional-selector="icon"
            status_span = choice_div.find(
                "span",
                attrs={
                    "data-functional-selector": "icon",
                    "aria-hidden": "false",
                },
            )

            is_correct = False
            if status_span:
                title_tag = status_span.find("title")
                if title_tag:
                    title_txt = title_tag.get_text(strip=True)
                    if "Correct" in title_txt:
                        is_correct = True
                    elif "Incorrect" in title_txt:
                        is_correct = False

            # Fallback: scan all SVG titles in this choice
            if status_span is None:
                for svg in choice_div.find_all("svg"):
                    t = svg.find("title")
                    if t:
                        tt = t.get_text(strip=True)
                        if "Correct" in tt:
                            is_correct = True
                            break
                        if "Incorrect" in tt:
                            is_correct = False
                            break

            options.append(opt_text)
            if is_correct:
                correct_answers.append(opt_text)

        # ---------- Decide question type ----------
        if len(options) == 2 and set(options) == {"True", "False"}:
            q_type = "true_false"
            correct_bool = (correct_answers[0] == "True") if correct_answers else False
            q_obj = {
                "id": qid,
                "type": q_type,
                "question": q_text,
                "correct_answer": correct_bool,
            }
        else:
            q_type = "multiple_choice"
            q_obj = {
                "id": qid,
                "type": q_type,
                "question": q_text,
                "options": options,
                "correct_answers": correct_answers,
            }

        questions.append(q_obj)
        qid += 1

    return questions


def main():
    if len(sys.argv) < 3:
        print("Usage: python extract_kahoot_to_json.py input.html output.json")
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2]

    with open(in_file, "r", encoding="utf-8", errors="ignore") as f:
        html_text = f.read()

    questions = extract_questions(html_text)

    data = {
        "quiz_title": in_file.split("/")[-1].replace(".html", ""),
        "questions": questions,
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(questions)} questions → {out_file}")


if __name__ == "__main__":
    main()
