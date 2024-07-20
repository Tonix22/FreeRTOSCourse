import json
from datetime import datetime, timedelta

# Helper function to add days, skipping weekends
def add_weekdays(start_date, num_days):
    current_date = start_date
    while num_days > 0:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:  # Monday to Friday are considered
            num_days -= 1
    return current_date


def generate_gantt_content(weeks, start_date):
    content = "@startgantt\nsaturday are closed\nsunday are closed\n\n"
    content += f"Project starts the {start_date.strftime('%dth of %B %Y')}\n\n"
    current_date = start_date
    
    for i, week in enumerate(weeks):
        week_title = f"[Week {week['weekNumber']}: {week['title']}]"
        week_ref = f"[W{i+1}]"
        
        # Start the first week on the second day to skip Monday
        if i == 0:
            content += f"{week_title} as {week_ref} starts at {current_date.strftime('%Y-%m-%d')} and lasts 1 day\n"
        else:
            content += f"{week_title} as {week_ref} starts 6 days after [W{i}]'s end and lasts 1 day\n"

        # Check if there's an evaluation for the week and add it
        if 'evaluation' in week:
            content += f"[{week['evaluation']}] happens at {week_ref}'s end\n"
        
        # Add 6 days to skip weekends
        current_date = add_weekdays(current_date, 6)
    
    content += "@endgantt\n"
    return content


def generate_latex(weeks):
    latex_content = "\\begin{enumerate}[label=\\textbf{Week \\arabic*:}]\n"
    for week in weeks:
        latex_content += f"\\item \\textbf{{ {week['title']} }}\n"
        latex_content += "\\begin{itemize}\n"
        for topic in week.get('topics', []):
            latex_content += f"  \\item {topic}\n"
        if 'subtopics' in week:
            latex_content += "  \\begin{itemize}\n"
            for subtopic in week['subtopics']:
                latex_content += f"    \\item {subtopic}\n"
            latex_content += "  \\end{itemize}\n"
        latex_content += "\\end{itemize}\n"
    latex_content += "\\end{enumerate}\n"
    return latex_content

def main():
    with open('/home/tonix/Documents/FreeRTOSCourse/Documentation/CourseContent/agenda.json', 'r') as file:
        course_data = json.load(file)
    
    # Filter the data for part 1 and part 2 planning
    part1_weeks = course_data["weeks"][:11]
    part2_weeks = course_data["weeks"][11:]
    
    # Define the start date of the project
    start_date = datetime.strptime("2024-08-05", "%Y-%m-%d")
    # Generate the Gantt chart content for Part 1
    gantt_content_part1 = generate_gantt_content(part1_weeks, start_date)
    # Save to file
    with open("PlanningPart1.puml", "w") as file:
        file.write(gantt_content_part1)

    # Define the start date of the project
    start_date = datetime.strptime("2024-10-23", "%Y-%m-%d")
    # Generate the Gantt chart content for Part 1
    gantt_content_part1 = generate_gantt_content(part2_weeks, start_date)
    # Save to file
    with open("PlanningPart2.puml", "w") as file:
        file.write(gantt_content_part1)
    
    latex_output = generate_latex(course_data['weeks'])
    with open('agenda.tex', 'w') as file:
        file.write(latex_output)

if __name__ == "__main__":
    main()
