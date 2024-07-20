import json
from datetime import datetime, timedelta

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
    with open('agenda.json', 'r') as file:
        course_data = json.load(file)
    
    latex_output = generate_latex(course_data['weeks'])
    with open('agenda.tex', 'w') as file:
        file.write(latex_output)

if __name__ == "__main__":
    main()
