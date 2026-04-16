# Markdown Quiz Player

A local web app that uploads a markdown quiz file and renders it as an interactive quiz UI with:
- option selection
- hint reveal
- answer submission
- instant correctness feedback
- detailed rationale reveal

The site is a unified dashboard that handles both study guide generation and interactive quiz building from a single interface.
It is live at: [https://testflow-zeta.vercel.app](https://testflow-zeta.vercel.app)

## Tech Stack

- Backend: FastAPI (`main.py`)
- Frontend: Unified Dashboard (`index.html`)
- Local server: Uvicorn

## Run Locally via terminal

From this folder (`markdown_quiz_app`):

```bash
pip install -r requirements.txt
python main.py
```

Open in browser:

- `http://127.0.0.1:8000` (Home / Guide Generator / Quiz Builder)

Run locally from this folder with:

- `python -m uvicorn api.main:app --reload`

## How To Use

1. Start the app (`python main.py`).
2. Open the page in your browser.
3. Drag-and-drop a `.md` quiz file (or click the upload zone).
4. Answer questions interactively:
   - pick A/B/C/D
   - click `Show Hint`
   - click `Submit Answer`
   - view correctness and rationale
   - navigate with `Previous` / `Next`

The dashboard provides a dual-column workflow:
- **Left Column**: Generates and renders a structured study guide from a URL.
- **Right Column**: Builds a high-depth interactive quiz based on the generated source.

## Accepted Markdown File Type

The parser only accepts:
- file extension: `.md`
- text encoding: UTF-8
- structure: strict quiz format described below

If the structure does not match, the backend returns a parse error with the question number.

## Required Markdown Structure (Strict)

Each question must follow this exact pattern.

### 1) Question Header

```md
### Question 1: Your Question Title
```

### 2) Question Body

- Normal markdown paragraph text
- Optional fenced code blocks are supported (for example ` ```html `)

### 3) Multiple Choice Options

Exactly 4 options, in this order:

```md
- A) Option text
- B) Option text
- C) Option text
- D) Option text
```

### 4) Hint Block (must match exactly)

```md
<details><summary><b>Hint</b></summary>
Hint text here.
</details>
```

### 5) Answer + Rationale Block (must match exactly)

```md
<details><summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**
- A) Why A is wrong/correct
- B) Why B is correct
- C) Why C is wrong/correct
- D) Why D is wrong/correct

</details>
```

### 6) Divider Between Questions

```md
---
```

## Full Single-Question Template

Copy this and repeat per question:

```md
### Question 1: Example Title

Write your question body here. You can include code blocks.

```html
<input type="email" required />
```

- A) First option
- B) Second option
- C) Third option
- D) Fourth option

<details><summary><b>Hint</b></summary>
Think about built-in browser validation behavior.
</details>

<details><summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** B

**Rationale:**
- A) Incorrect because ...
- B) Correct because ...
- C) Incorrect because ...
- D) Incorrect because ...

</details>

---
```

## Agent Skills To Generate Compatible Markdown

Use these skills when generating quiz files so output is closest to the accepted structure:

1. `generate_comprehensive_quiz`
- Best choice for producing quiz-style markdown with options, hints, and rationale.
- After generation, ensure headings and details blocks exactly match the required strings above.

2. `create_study_guide` (optional pre-step)
- Use this first if you need to build source material.
- Then use `generate_comprehensive_quiz` to convert study content into quiz format.

## Recommended Prompt For Quiz Generation

Use a prompt like this when invoking quiz generation:

OPTION1: 
```text
Generate quiz markdown using this exact format for every question:
- Header: ### Question [Number]: [Title]
- Four options exactly: - A), - B), - C), - D)
- Hint block exactly:
  <details><summary><b>Hint</b></summary>...</details>
- Answer block exactly:
  <details><summary><b>View Answer & Detailed Rationale</b></summary>
  **Correct Answer:** [A-D]
  **Rationale:**
  - A) ...
  - B) ...
  - C) ...
  - D) ...
  </details>
- Separate each question with ---
Output valid UTF-8 markdown.
```
OPTION2:
```text
create a quiz using C:\Users\andyf\Documents\GitHub\learn-js\guides\Advanced JS Objects

the files in this folder. 

a total number of 30 questions and save the quiz in the same path. use your generate_comprehensive_quiz skill
```

## Common Parse Errors and Fixes

- `Only .md files are accepted.`
  - Rename file extension to `.md`.

- `File must be UTF-8 encoded markdown.`
  - Re-save file as UTF-8.

- `Question X: expected 4 options ...`
  - Ensure exactly A/B/C/D option lines exist in order.

- `missing hint block` or `missing answer block`
  - Ensure the `<details><summary><b>...</b></summary>...</details>` text matches exactly.

- `missing '**Correct Answer:** [Letter]'`
  - Add a valid answer letter A-D.

- `missing '**Rationale:**' section`
  - Add rationale heading and bullet points.

## Project Files

- `api/main.py`: FastAPI server, markdown parser, and AI generating endpoints
- `index.html`: Unified Dashboard UI + persistence logic
- `requirements.txt`: Python dependencies
- `README.md`: usage and format guide
