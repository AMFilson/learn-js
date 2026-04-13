---
name: generate_comprehensive_quiz
description: >
  Generate a comprehensive, high-depth practice quiz in Markdown format from
  technical documentation or study guides. This skill utilizes a multi-batch
  strategy to avoid token limits and enforces a strict structural template
  with interactive hints and bulleted rationales (Correct/Incorrect).
---

# Skill: Generate Comprehensive Quiz

## Overview

This skill converts technical resources (MDN documentation, study guides, textbooks) into a high-depth practice quiz. It is designed to both test knowledge and teach concepts through detailed "Why" rationales.

Key features:
1.  **Batching Strategy**: Mandatory 10-question batches to prevent hallucinations.
2.  **Gold Standard Structure**: Interactive toggles with `<details>` tags.
3.  **Instructional Depth**: Every rationale must explain why the correct answer is optimal AND why the distractors are incorrect.

---

## How to Use

To use this skill, the user must provide:
1.  **Source Material** (Local study guide files or MDN URLs).
2.  **Target Quantity** (Total number of questions, e.g., 60).
3.  **Output Path** (Where to save the quiz file).

The generation process **MUST** be performed in batches of 10 to ensure maximum rationale depth.

---

## Execution Workflow

### Step 1 — Resource Synthesis
Read the target source material (URLs via `read_url_content` or local files via `view_file`). Identify the "immutable facts" and key exam-critical concepts.

### Step 2 — Batch Generation (Q1-10)
Generate the first batch of 10 questions. 
**Crucial**: Do NOT generate more than 10 questions at a time. The high depth required for rationales will exceed context limits and lead to "abbreviated" (low quality) answers if you attempt 20+ questions in one turn.

### Step 3 — User Checkpoint & Appending
After each batch:
1.  Save the content to the target file.
2.  Stop and request user feedback/approval to proceed to the next batch.
3.  Continue until the target question count (e.g., 60 questions) is reached.

---

## Naming Convention

Follow the project's naming hierarchy:
`quiz_[topic_name].md`

Example:
- `quiz_web_forms.md`
- `quiz_js_dynamic_scripting.md`

---

## The "Gold Standard" Question Template

Every single question must follow this exact structure to ensure a premium user experience.

```markdown
### Question N: [Concise Title]

[Technical Scenario / Problem Description]

- A) [Option A]
- B) [Option B]
- C) [Option C]
- D) [Option D]

<details>
<summary><b>Hint</b></summary>
[A conceptual hint that nudges the user toward the answer without giving it away.]
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** [Letter]

**Rationale:**

- **Why [Letter] is optimal/correct:** [Deep technical explanation of the successful outcome.]
- **Why [Distractor 1] is incorrect:** [Explanation of the technical violation or error.]
- **Why [Distractor 2/3] are incorrect:** [Explanation of why these are sub-optimal or fictitious.]
</details>

---
```

---

## Quality & Validation Rules

### 1. Depth of Rationale
-   **No one-liners**: Rationales must be at least 2-3 sentences per bullet point.
-   **Technical jargon**: Use correct terminology (e.g., "Void element," "Reflow," "Casdcading inheritance").
-   **Production Context**: Relate the explanation to real-world production performance or security when applicable.

### 2. Interaction Toggles
-   Use `<details>` and `<summary>` tags strictly.
-   Ensure a blank line exists between the summary and the start of the rationale content to prevent Markdown parsing errors.

### 3. Diversity of Difficulty
-   **Recall**: Basic syntax check.
-   **Application**: "A developer does X, what happens...?"
-   **Diagnosis**: "Why does this code fail to...?"
-   **Hybrid**: "What is the difference between X and Y regarding Z?"

### 4. Hallucination Prevention
-   If you approach your token limit during a batch, stop immediately and prompt for continuation.
-   Never sacrifice rationale depth for question quantity. If you cannot provide a detailed "Why incorrect" section, you must split the batch further.

---

---

## Example Invocation

When asked to create a quiz, follow these steps:

1.  **Preparation**:
    *   Assess the source material (e.g., 5 study guides in `guides/Web Forms/`).
    *   Determine the file name (e.g., `guides/Web Forms/quiz_web_forms.md`).

2.  **Batching Context**:
    *   "I will generate 60 questions for the Web Forms module. I'll proceed in 6 batches of 10 to ensure technical depth. Batch 1 starting now."

3.  **Turn 1 (Generation)**:
    *   `view_file` or `read_url_content` for the resources.
    *   Generate Q1-10 using the [Gold Standard Template](#the-gold-standard-question-template).
    *   `write_to_file` the new quiz.
    *   Stop and ask: "Batch 1 complete (Q1-10). Proceed to Batch 2?"

4.  **Turns 2-6 (Appending)**:
    *   Upon approval, generate the next 10 questions.
    *   `multi_replace_file_content` to append at the end of the file.
    *   Stop and ask for the next batch.

5.  **Turn 7 (Polish)**:
    *   Perform the [Final Review Checklist](#final-review-checklist) and standardize any whitespace.
