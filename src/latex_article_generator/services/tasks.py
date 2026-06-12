"""CrewAI task factories for all four pipeline tasks (tasks 011–014)."""

from crewai import Task


def build_research_task(topic: str, sections: list[str], agent) -> Task:
    """Return the research Task for the given topic."""
    sections_str = ", ".join(sections)
    return Task(
        description=(
            f"Research the topic: '{topic}'.\n"
            f"Focus on these sections: {sections_str}.\n"
            "Gather credible academic sources, key findings, and relevant data. "
            "Produce a structured research brief with source citations."
        ),
        expected_output=(
            "A structured research brief containing:\n"
            "1. Key concepts and definitions\n"
            "2. Current state of the art\n"
            "3. At least 5 cited academic sources (author, title, year, venue)\n"
            "4. Key findings relevant to each requested section"
        ),
        agent=agent,
    )


def build_writing_task(topic: str, sections: list[str], agent, research_task: Task) -> Task:
    """Return the writing Task; depends on research_task for context."""
    sections_str = ", ".join(sections)
    return Task(
        description=(
            f"Write the following sections of an academic article about '{topic}':\n"
            f"{sections_str}\n\n"
            "Use the research brief from the previous task. "
            "Write in academic English. Include in-text citations in [Author, Year] format. "
            "Keep each section concise (200-300 words). "
            "For the methodology section, include a comparison table of at least 3 ML algorithms. "
            "For the results section, reference a bar chart of accuracy metrics. "
            "Include at least one mathematical formula (e.g. loss function or performance metric)."
        ),
        expected_output=(
            "Complete prose for each requested section, clearly delimited by section name. "
            "Each section must be at least 300 words. "
            "Citations must be in the format [Author, Year]."
        ),
        agent=agent,
        context=[research_task],
    )


def build_review_task(agent, writing_task: Task) -> Task:
    """Return the review Task; depends on writing_task for context."""
    return Task(
        description=(
            "Review the drafted article sections for:\n"
            "1. Academic quality and clarity\n"
            "2. Logical flow between sections\n"
            "3. Citation accuracy and completeness\n"
            "4. Factual consistency with the research brief\n\n"
            "Produce the final, improved version of the article text. "
            "Keep each section focused and complete."
        ),
        expected_output=(
            "The final, revised article text with all sections complete. "
            "Include a brief review summary (max 150 words) at the top noting what was changed."
        ),
        agent=agent,
        context=[writing_task],
    )


def build_formatting_task(
    agent, review_task: Task, *, graph_path: str = "", bib_path: str = ""
) -> Task:
    """Return the LaTeX formatting Task; depends on review_task for context."""
    bib = bib_path or "references.bib"
    graph_cmd = (
        r"\includegraphics[width=0.8\textwidth]{" + graph_path + "}"
        if graph_path
        else r"% graph placeholder"
    )
    return Task(
        description=(
            "Convert the reviewed article into a COMPLETE, COMPILABLE XeLaTeX document.\n"
            "STRICT RULES:\n"
            "- Output raw LaTeX ONLY — no ```latex fences, no explanatory text.\n"
            r"- First character must be '\', last line must be \end{document}." + "\n"
            "- Keep sections concise to avoid truncation.\n\n"
            "PREAMBLE (use verbatim):\n"
            r"\documentclass[12pt,a4paper]{article}" + "\n"
            r"\usepackage{fontspec}" + "\n"
            r"\setmainfont{Times New Roman}" + "\n"
            r"\usepackage{polyglossia}" + "\n"
            r"\setmainlanguage{english}" + "\n"
            r"\setotherlanguage{hebrew}" + "\n"
            r"\newfontfamily\hebrewfont[Script=Hebrew]{Arial}" + "\n"
            r"\usepackage[a4paper,margin=2.5cm]{geometry}" + "\n"
            r"\usepackage{setspace}\onehalfspacing" + "\n"
            r"\usepackage{graphicx,float,tikz,amsmath,amssymb,booktabs}" + "\n"
            r"\usetikzlibrary{shapes,arrows,positioning}" + "\n"
            r"\usepackage{fancyhdr}\pagestyle{fancy}\fancyhf{}" + "\n"
            r"\setlength{\headheight}{14.5pt}" + "\n"
            r"\fancyhead[L]{Machine Learning in Healthcare}\fancyhead[R]{\thepage}" + "\n"
            r"\usepackage[backend=biber,style=ieee,url=false,doi=false]{biblatex}" + "\n"
            r"\addbibresource{" + bib + "}\n"
            r"\usepackage[hidelinks]{hyperref}" + "\n\n"
            "REQUIRED STRUCTURE (all 9 items must appear):\n"
            r"1. \title{...}\author{...}\date{...}\begin{document}\maketitle\tableofcontents\newpage"
            + "\n"
            r"2. \section*{תקציר} — 2 paragraphs of Hebrew inside \begin{hebrew}...\end{hebrew}"
            + "\n"
            r"3. \section{Introduction} — use \autocite{Topol2019} and \autocite{Rajpurkar2022}"
            + "\n"
            r"4. \section{Methodology} — include booktabs TABLE and display MATH FORMULA"
            + "\n"
            "5. " + r"\section{Results}" + " — embed: " + graph_cmd + "\n"
            r"6. \section{Conclusion}" + "\n"
            r"7. TikZ flowchart: \begin{figure}[H]\begin{tikzpicture}...\end{tikzpicture}\end{figure}"
            + "\n"
            r"8. \printbibliography" + "\n"
            r"9. \end{document}" + "\n\n"
            "Citation keys available: "
            "Topol2019 Rajpurkar2022 ONC2021 GrandView2022 Sheller2020 Komorowski2018"
        ),
        expected_output=(
            r"A complete LaTeX document starting with \documentclass[12pt,a4paper]{article} "
            r"and ending with \end{document}. "
            "Contains Hebrew abstract, table, formula, graph figure, TikZ diagram, bibliography. "
            "No markdown code fences."
        ),
        agent=agent,
        context=[review_task],
    )
