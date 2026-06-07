"""Base LaTeX preamble template — task 021."""

PREAMBLE_TEMPLATE = r"""
\documentclass[12pt,a4paper]{{article}}

% Encoding and language
\usepackage{{fontspec}}
\usepackage{{polyglossia}}
\setmainlanguage{{english}}
\setotherlanguage{{hebrew}}
\newfontfamily\hebrewfont[Script=Hebrew]{{David CLM}}

% Layout
\usepackage{{geometry}}
\geometry{{margin=2.5cm}}
\usepackage{{setspace}}
\onehalfspacing

% Graphics and diagrams
\usepackage{{graphicx}}
\usepackage{{tikz}}
\usetikzlibrary{{shapes,arrows,positioning}}
\usepackage{{float}}

% Math
\usepackage{{amsmath,amssymb}}

% Bibliography
\usepackage[backend=biber,style=ieee]{{biblatex}}
\addbibresource{{{bib_file}}}

% Hyperlinks
\usepackage{{hyperref}}
\hypersetup{{colorlinks=true,linkcolor=blue,citecolor=blue}}

% Headers/Footers
\usepackage{{fancyhdr}}
\pagestyle{{fancy}}

\title{{{title}}}
\author{{{author}}}
\date{{{date}}}
"""


class LatexTemplate:
    def render_preamble(self, title: str, author: str, date: str, bib_file: str) -> str:
        """Render the preamble with the given metadata."""
        return PREAMBLE_TEMPLATE.format(
            title=title, author=author, date=date, bib_file=bib_file
        )
