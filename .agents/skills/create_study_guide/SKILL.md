---
name: create_study_guide
description: >
  Generate a comprehensive, exam-ready study guide in Markdown format from any
  URL (MDN article, documentation page, textbook chapter, etc.). Fetches the
  page content, synthesises it into a structured .md file, and saves it to a
  user-specified location using the project's naming convention.
---

# Skill: Create Study Guide

## Overview

This skill turns any webpage into a comprehensive, exam-ready Markdown study guide.
It is used by invoking it with two inputs:

1. **URL** — the webpage to read and synthesise
2. **Output folder** — the directory to save the guide into

The saved file follows the project's naming convention (see §Naming Convention below).

---

## Execution Steps

### Step 1 — Read the Source Page

Use the `read_url_content` tool to fetch the page at the provided URL.
Then use `view_file` to read the saved content from the returned file path.
Read as many lines as needed to capture the full article body (not just headers).

### Step 2 — Identify Naming Convention

Check the output folder for existing study guides to confirm the naming pattern.
The standard convention in this project is:

```
[prefix]_[topic]_study_guide.md
```

Examples:
- `js_arrays_study_guide.md`            (JavaScript topic, in /guides/Dynamic scripting with JS/)
- `html_forms_study_guide.md`           (HTML topic, in /guides/)
- `html_your_first_form_study_guide.md` (HTML topic, in /guides/)

**Deriving the filename:**
- Choose a prefix that reflects the subject area (`js_`, `html_`, `css_`, etc.)
- Use the article's main topic as the stem, lowercased, words joined with `_`
- Always end with `_study_guide.md`

### Step 3 — Write the Study Guide

Use `write_to_file` to create the `.md` file at the correct path.
The file MUST follow the document structure below exactly.

---

## Document Structure (Template)

Every generated study guide must contain ALL of the following sections in order:

```markdown
# 📚 [Topic Title] — Exam Study Guide
**Source:** [MDN / full URL here]

---

## Executive Summary

[3 sentences: (1) what the page is about, (2) the central concept or mechanism,
(3) the most important takeaway for an exam context.]

---

## Core Pillars

### 1. [Main Theme Title]
[Explanation using bullet points and/or sub-headings. Break complex logic into
clear steps. Use code blocks for any HTML/JS/CSS syntax.]

### 2. [Next Theme Title]
...

[Continue for all major themes in the article — typically 6-12 pillars.]

---

## Technical Deep-Dive

### Logic Walkthrough: [Name the scenario being walked through]

[Step-by-step breakdown of the most complex concept on the page.
Use code blocks to show input → output. Annotate with comments.
Add as many walkthroughs as needed for distinct complex topics.]

---

## Key Terminology Bank

| Term | Exam-Ready Definition |
|---|---|
| **`term`** | One-sentence, precise definition written as if answering an exam question. |
...

[Minimum 15 terms. Include all jargon, attribute names, element names,
and concepts introduced in the article.]

---

## Watch Out For...

1. **[Misconception 1]** — [Explain why it's wrong and what the truth is.]
2. **[Misconception 2]** — ...

[Minimum 8 pitfalls. Focus on subtle distinctions, default values that surprise
people, and things that differ from intuitive expectations.]

---

## Active Recall — Check for Understanding

**Instructions:** Answer each question without looking at the guide. Check answers below.

---

**Q1.** [Question targeting a core concept]

**Q2.** [Question requiring code recall or writing]

**Q3.** [Question that probes a common misconception]

**Q4.** [Question requiring a comparison between two related things]

**Q5.** [Question that integrates multiple concepts from the page]

---

## Answer Key

---

**A1.** [Full, detailed answer. Do not just repeat the question — provide the
complete explanation a grader would give full marks for.]

**A2.** [Include example code where appropriate]

**A3.** ...

**A4.** [Use a comparison table if the question asks for differences]

**A5.** ...
```

---

## Content Guidelines

### Executive Summary
- Exactly 3 sentences.
- Sentence 1: State the page's topic.
- Sentence 2: Name the central mechanism, element, or concept the page revolves around.
- Sentence 3: State the most exam-critical takeaway.

### Core Pillars
- Each `##` section = one major theme from the article (e.g., one element, one rule system, one concept group).
- Use `###` sub-headers for sub-topics within a theme.
- Prefer bullet points over paragraphs for scannability.
- Include **all code examples** from the article. Format in fenced code blocks with `html`, `js`, or `css` language tags.
- Bold all critical keywords on first use: `**keyword**`.
- For complex tables (e.g., attribute reference tables), always use Markdown table format.

### Technical Deep-Dive
- Required if the page contains: submission behaviour, event flow, algorithm steps, HTTP mechanics, or any process with multiple sequential stages.
- Each walkthrough must show: the setup (HTML/JS code), a step-by-step narration, and the output (URL, console result, server payload, etc.).
- Comment each code line that requires explanation.

### Key Terminology Bank
- Every element name, attribute name, method name, CSS property, and concept introduced in the article must appear as a row.
- Definitions must be exam-ready: precise, one-sentence, include the critical constraint or nuance.
- Use backtick-formatting for code terms: `` **`type`** ``.

### Watch Out For...
- Focus on:
  - Default values that deviate from what seems intuitive
  - Distinctions between two things that look similar (e.g., `readonly` vs `disabled`)
  - Things that are NOT done (e.g., "unchecked checkboxes are not submitted")
  - Void elements / closing tag mistakes
  - Security implications
  - Submission behaviour differences
  - Fallback behaviour
- Each pitfall should: (a) name the trap, (b) state the incorrect assumption, (c) state the correct truth.

### Active Recall Questions
- Q1: Conceptual recall (no code required)
- Q2: Code writing or identification
- Q3: Contrast question — "what is the difference between X and Y"
- Q4: Behaviour prediction — "what happens when..."
- Q5: Integrated multi-concept question
- Answers must be at the BOTTOM of the document (not collapsed/hidden) and must be comprehensive — full marks answers, not one-liners.

---

## Tone & Style Rules

- **Professional and concise** — write like a senior technical writer, not a teacher explaining to a beginner.
- **Logically dense** — prioritise information density. Avoid filler phrases ("It's important to note that...").
- **Scannable** — a student should be able to review the whole document in 10 minutes.
- **Bolding** — bold critical terms, key distinctions, and anything that would likely appear on an exam.
- **No fluff** — every sentence must convey a testable fact or actionable understanding.

---

## Example Invocation

When the user provides a URL and folder path, follow these steps:

```
1. read_url_content(url)
2. view_file(saved_content_path) — read enough lines to capture the full article
3. Determine the output filename using §Naming Convention
4. write_to_file(full_output_path, study_guide_content)
```

**Example:**
- URL: `https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Basic_native_form_controls`
- Output folder: `c:\Users\andyf\Documents\GitHub\learn-js\guides\`
- Derived filename: `html_basic_native_form_controls_study_guide.md`
- Full path written: `c:\Users\andyf\Documents\GitHub\learn-js\guides\html_basic_native_form_controls_study_guide.md`
