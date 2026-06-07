# Prompt Engineering Log

Records the prompt design and iteration history for each CrewAI agent and task.

---

## Agent: ResearcherAgent

### Prompt v1.0 (initial)
**Role:** Researcher  
**Goal:** Research the topic.  
**Backstory:** You are a researcher.

**Problem observed:** The agent returned general web summaries and blog posts rather than academic papers. Source citations were missing or in informal format. The research brief lacked structure.

### Prompt v1.1 (revised)
**Role:** Academic Researcher  
**Goal:** Thoroughly investigate the given topic and gather credible, up-to-date academic and technical sources.  
**Backstory:** You are a meticulous academic researcher with expertise in literature review, source verification, and structured knowledge synthesis.

**Why this works better:** Explicitly labelling the role "Academic Researcher" and specifying "credible academic and technical sources" constrains the agent to scholarly venues (journals, conference proceedings) over informal web content. The backstory adds domain framing that guides output structure.

---

## Agent: WriterAgent

### Prompt v1.0 (initial)
**Role:** Writer  
**Goal:** Write an article about the topic.  
**Backstory:** You are a writer.

**Problem observed:** Output was conversational in tone, lacked in-text citations, and section lengths were inconsistent (some under 100 words). The agent ignored the research brief entirely in one test run.

### Prompt v1.1 (revised)
**Role:** Academic Writer  
**Goal:** Draft clear, well-structured academic article sections based on the provided research brief.  
**Backstory:** You are an experienced academic writer skilled in producing publication-ready prose for computer science and engineering papers.

**Why this works better:** Anchoring the goal to "the provided research brief" forces the agent to consume context from the research task. Specifying "computer science and engineering papers" narrows the style to formal academic English with citation conventions.

---

## Agent: ReviewerAgent

### Prompt v1.0 (initial)
**Role:** Reviewer  
**Goal:** Review the article.  
**Backstory:** You are a reviewer.

**Problem observed:** The reviewer only returned a bullet-point list of suggestions without producing improved text. The formatter received no usable input as a result.

### Prompt v1.1 (revised)
**Role:** Academic Reviewer  
**Goal:** Review the drafted article for academic quality, logical flow, and citation accuracy — then produce an improved final version.  
**Backstory:** You are a senior academic peer reviewer with experience in IEEE and ACM publication standards. You improve articles, not just critique them.

**Why this works better:** Explicitly requiring the reviewer to "produce an improved final version" (not just critique) ensures the output is usable downstream. Referencing IEEE/ACM standards sets concrete quality benchmarks for the agent.

---

## Agent: LaTeXFormatterAgent

### Prompt v1.0 (initial)
**Role:** Formatter  
**Goal:** Format the article as LaTeX.  
**Backstory:** You know LaTeX.

**Problem observed:** The agent produced incomplete preambles, omitted `\begin{document}`, and did not wrap Hebrew text in RTL directives. The output was not compilable.

### Prompt v1.1 (revised)
**Role:** LaTeX Formatter  
**Goal:** Convert reviewed article text into a complete, compilable LuaLaTeX document with proper RTL support for Hebrew content.  
**Backstory:** You are an expert LaTeX typesetter specialising in multilingual academic documents using LuaLaTeX, polyglossia, and biblatex. You produce documents that compile without errors on the first attempt.

**Why this works better:** Naming LuaLaTeX (not just LaTeX) prevents the agent from using pdflatex-only packages. Explicitly mentioning "RTL support for Hebrew" ensures the agent wraps Hebrew text correctly. "Compile without errors on the first attempt" creates an internal quality gate.

---

## Task: Research Task

### Description v1.0 (initial)
Research the topic and find sources.

**Problem observed:** Agent collected only 2 sources (requirement is ≥ 5) and did not structure the brief by section.

### Description v1.1 (revised)
```
Research the topic: '{topic}'.
Focus on these sections: {sections_str}.
Gather credible academic sources, key findings, and relevant data.
Produce a structured research brief with source citations.
```

**Expected output refined to specify:**
- Key concepts and definitions
- Current state of the art
- At least 5 cited academic sources (author, title, year, venue)
- Key findings per requested section

**Why this works better:** The section list in the description focuses the agent on coverage. The explicit "at least 5 cited sources" requirement in `expected_output` gave the agent a measurable goal.

---

## Task: Writing Task

### Description v1.0 (initial)
Write the article.

**Problem observed:** Sections were too short (< 100 words) and citations used URLs instead of author-year format.

### Description v1.1 (revised)
```
Write the following sections of an academic article about '{topic}':
{sections_str}

Use the research brief from the previous task as your source.
Write in clear academic English. Include in-text citations.
If a section requires Hebrew content, write it in Hebrew with proper RTL formatting.
```

**Expected output refined to require:**
- At least 300 words per section
- Citations in `[Author, Year]` format

**Why this works better:** The 300-word minimum in `expected_output` gives the agent a concrete length target. Specifying citation format (`[Author, Year]`) eliminates URL-based references.

---

## Task: Review Task

### Description v1.0 (initial)
Review the article and provide feedback.

**Problem observed:** Reviewer returned only feedback notes. Formatter had no improved text to work with.

### Description v1.1 (revised)
```
Review the drafted article sections for academic quality, logical flow,
citation accuracy, factual consistency, and Hebrew/RTL correctness.
Produce an improved, final version with all issues addressed.
```

**Expected output refined to include:**
- The complete improved article text
- A brief review summary (max 200 words) at the top

**Why this works better:** Requiring the "complete improved article text" in the output forces the reviewer to deliver usable content to the formatter, not just notes.

---

## Task: Formatting Task

### Description v1.0 (initial)
Format the article as LaTeX.

**Problem observed:** Agent produced LaTeX fragments, not a complete document. RTL content was not wrapped.

### Description v1.1 (revised)
```
Convert the reviewed article text into a complete, compilable LaTeX document.
Structure each section with proper LaTeX environments.
Apply RTL formatting (\begin{RTL}...\end{RTL}) for any Hebrew content.
Include a full preamble with all required packages.
```

**Expected output refined to specify:**
- Must start with `\documentclass{article}`
- Must compile with LuaLaTeX without errors

**Why this works better:** The `\documentclass` requirement prevents the agent from returning a document fragment. The LuaLaTeX constraint prevents pdflatex-incompatible packages.
