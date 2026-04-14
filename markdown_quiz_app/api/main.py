from __future__ import annotations

from collections import Counter
import html as html_module
import re
from pathlib import Path
from typing import List, Optional
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


class QuizOption(BaseModel):
    letter: str
    text: str


class RationalePoint(BaseModel):
    letter: Optional[str] = None
    text: str


class QuizQuestion(BaseModel):
    number: int
    title: str
    body_markdown: str
    options: List[QuizOption]
    hint_markdown: str
    correct_answer: str
    rationale: List[RationalePoint]


class ParsedQuiz(BaseModel):
    source_file: str
    question_count: int
    questions: List[QuizQuestion]


class StudyGuideRequest(BaseModel):
    url: str
    subject: str = "General"
    topic: Optional[str] = None


class StudyGuideResponse(BaseModel):
    source_url: str
    source_title: str
    filename: str
    markdown: str


class QuizPromptRequest(BaseModel):
    source_url: Optional[str] = None
    source_text: Optional[str] = None
    subject: str = "General"
    topic: Optional[str] = None
    batch_start: int = 1


class QuizPromptResponse(BaseModel):
    source_label: str
    source_title: str
    batch_range: str
    filename: str
    prompt_markdown: str


app = FastAPI(title="Markdown Quiz Parser", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


QUESTION_HEADER_RE = re.compile(r"^###\s+Question\s+(\d+)\s*:\s*(.+)$", re.MULTILINE)
OPTION_START_RE = re.compile(r"^\s*-\s*([A-D])\)\s*(.*)$", re.MULTILINE)
HINT_RE = re.compile(
    r"<details>\s*<summary>\s*<b>Hint</b>\s*</summary>(.*?)</details>",
    re.DOTALL,
)
ANSWER_BLOCK_RE = re.compile(
    r"<details>\s*<summary>\s*<b>View Answer\s*&\s*Detailed Rationale</b>\s*</summary>(.*?)</details>",
    re.DOTALL,
)
CORRECT_ANSWER_RE = re.compile(r"\*\*Correct Answer:\*\*\s*([A-D])")
RATIONALE_SECTION_RE = re.compile(r"\*\*Rationale:\*\*\s*(.*)$", re.DOTALL)
RATIONALE_LETTER_BULLET_RE = re.compile(r"^\s*-\s*([A-D])\)\s+(.+?)\s*$", re.MULTILINE)
RATIONALE_GENERIC_BULLET_RE = re.compile(r"^\s*-\s+(.+?)\s*$", re.MULTILINE)
SPLIT_QUESTIONS_RE = re.compile(r"^\s*---\s*$", re.MULTILINE)
TITLE_RE = re.compile(r"(?is)<title[^>]*>(.*?)</title>")
HEADING_RE = re.compile(r"(?is)<h([1-3])[^>]*>(.*?)</h\1>")
PRE_RE = re.compile(r"(?is)<pre[^>]*>(.*?)</pre>")
SCRIPT_STYLE_RE = re.compile(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>")
BLOCK_TAG_RE = re.compile(r"(?is)</?(?:p|div|section|article|header|footer|main|aside|nav|li|ul|ol|table|tr|td|th|pre|blockquote|h[1-6])[^>]*>")
BR_RE = re.compile(r"(?is)<br\s*/?>")
TAG_RE = re.compile(r"(?is)<[^>]+>")
CODE_TOKEN_RE = re.compile(r"`([^`]{2,80})`")
WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9_-]{3,}\b")


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", text.strip().lower())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "study_guide"


def _clean_text(value: str) -> str:
    value = html_module.unescape(value)
    value = TAG_RE.sub(" ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _extract_page_payload(url: str) -> dict:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise HTTPException(status_code=400, detail="Enter a valid http or https URL.")

    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
        },
    )

    try:
        with urlopen(request, timeout=20) as response:
            raw_html = response.read().decode("utf-8", errors="ignore")
    except (HTTPError, URLError, TimeoutError) as exc:
        raise HTTPException(status_code=400, detail=f"Failed to fetch the URL: {exc}") from exc

    title_match = TITLE_RE.search(raw_html)
    source_title = _clean_text(title_match.group(1)) if title_match else ""

    headings = [_clean_text(match.group(2)) for match in HEADING_RE.finditer(raw_html)]
    code_samples = []
    for match in PRE_RE.finditer(raw_html):
        sample = html_module.unescape(match.group(1))
        sample = re.sub(r"(?is)^<code[^>]*>", "", sample)
        sample = re.sub(r"(?is)</code>$", "", sample)
        sample = sample.strip("\n")
        if sample:
            code_samples.append(sample)

    text_only = SCRIPT_STYLE_RE.sub(" ", raw_html)
    text_only = BR_RE.sub("\n", text_only)
    text_only = BLOCK_TAG_RE.sub("\n", text_only)
    text_only = TAG_RE.sub(" ", text_only)
    text_only = html_module.unescape(text_only)
    text_only = re.sub(r"\n{3,}", "\n\n", text_only)
    text_only = re.sub(r"[ \t]{2,}", " ", text_only)
    visible_lines = [line.strip() for line in text_only.splitlines() if line.strip()]
    visible_text = "\n".join(visible_lines)

    return {
        "title": source_title,
        "headings": headings,
        "code_samples": code_samples,
        "text": visible_text,
        "domain": parsed.netloc,
        "path": parsed.path,
    }


def _pick_topic_title(payload: dict, override: Optional[str], subject: str, url: str) -> str:
    if override and override.strip():
        return override.strip()
    if payload["title"]:
        return payload["title"]
    path_bits = [bit for bit in payload["path"].split("/") if bit]
    if path_bits:
        return path_bits[-1].replace("-", " ").replace("_", " ").title()
    return f"{subject.title()} Topic"


def _pick_key_phrases(payload: dict, limit: int = 12) -> List[str]:
    phrases: List[str] = []
    for heading in payload["headings"]:
        if heading and heading not in phrases:
            phrases.append(heading)
    for token in CODE_TOKEN_RE.findall(payload["text"]):
        token = token.strip()
        if token and token not in phrases:
            phrases.append(token)
    if len(phrases) < limit:
        words = [word for word in WORD_RE.findall(payload["text"])]
        counts = Counter(word.lower() for word in words)
        for word, _ in counts.most_common():
            cleaned = word.replace("_", " ").strip()
            if len(cleaned) < 4:
                continue
            title = cleaned.title()
            if title not in phrases:
                phrases.append(title)
            if len(phrases) >= limit:
                break
    return phrases[:limit]


def _detect_code_language(snippet: str) -> str:
    sample = snippet.lower()
    if "<" in sample and ">" in sample:
        return "html"
    if "function" in sample or "const " in sample or "let " in sample or "=>" in sample:
        return "js"
    if "{" in sample and ":" in sample and ";" not in sample:
        return "css"
    return "text"


def _render_source_excerpt(payload: dict, source_text: str, limit_chars: int = 12000) -> str:
    excerpt_parts: List[str] = []
    if payload.get("title"):
        excerpt_parts.append(f"Title: {payload['title']}")
    if payload.get("domain"):
        excerpt_parts.append(f"Domain: {payload['domain']}")
    if payload.get("headings"):
        excerpt_parts.append("Headings:")
        excerpt_parts.extend(f"- {heading}" for heading in payload["headings"][:20] if heading)
    if payload.get("code_samples"):
        excerpt_parts.append("Code Samples:")
        for sample in payload["code_samples"][:5]:
            excerpt_parts.append("```text")
            excerpt_parts.append(sample.strip()[:1600])
            excerpt_parts.append("```")

    if source_text.strip():
        excerpt_parts.append("Visible Text:")
        excerpt_parts.append(source_text.strip())
    elif payload.get("text"):
        excerpt_parts.append("Visible Text:")
        excerpt_parts.append(payload["text"])

    excerpt = "\n".join(excerpt_parts).strip()
    if len(excerpt) > limit_chars:
        excerpt = excerpt[:limit_chars].rstrip() + "\n[truncated for prompt size]"
    return excerpt


def _build_quiz_prompt_text(source_label: str, source_content: str, subject: str, topic_title: str, batch_start: int) -> str:
    batch_end = batch_start + 9
    batch_label = f"{batch_start}-{batch_end}"
    fenced_source = source_content if source_content.strip() else "[No source text was provided.]"
    fenced_source = fenced_source.replace("~~~", "~ ~ ~")

    return f"""# Role: TestFlow Quiz Architect
# Feature: High-Depth Technical Assessment Generator

## Objective
Convert technical documentation (provided via URL or text) into a "Gold Standard" practice quiz for the TestFlow web platform (https://testflow-zeta.vercel.app/).

## Operational Constraints
1. **Batching:** Generate exactly 10 questions per request.
2. **Technical Depth:** Every question must include a "Rationale" that explains the correct answer AND specifically why each distractor is incorrect/sub-optimal.
3. **Format:** Use strict Markdown with HTML `<details>` tags for interactivity.

## Input Data
- **Topic/Source:** {source_label}
- **Current Batch:** {batch_label}

## Source Material
~~~text
{fenced_source}
~~~

## Output Template (Strict Adherence)
For every question, follow this exact structure:

### Question [Number]: [Sub-topic Title]
[Provide a clear technical scenario or conceptual question.]

- A) [Option]
- B) [Option]
- C) [Option]
- D) [Option]

<details>
<summary><b>Hint</b></summary>
[Provide a conceptual nudge using technical terminology without revealing the answer.]
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** [Letter]

**Rationale:**
- **Why [Letter] is optimal:** [2-3 sentences using jargon like 'cascading,' 'idempotency,' or 'state management'.]
- **Why [Incorrect Option 1] is wrong:** [Specific technical violation explanation.]
- **Why [Incorrect Option 2] is wrong:** [Specific technical violation explanation.]
- **Why [Incorrect Option 3] is wrong:** [Specific technical violation explanation.]
</details>

---

## Quality Guardrails
- **No Surface-Level Content:** Do not use "All of the above" or "None of the above."
- **Production-Ready:** Relate rationales to real-world performance, security, or accessibility (WCAG).
- **Naming:** If providing a downloadable file, name it: `quiz_{_slugify(topic_title)}.md`.
- **Formatting:** Ensure a blank line exists between `<summary>` and the rationale text to ensure proper Markdown rendering on the TestFlow frontend.
"""


def build_quiz_prompt_markdown(
    source_url: Optional[str],
    source_text: Optional[str],
    subject: str,
    topic_override: Optional[str],
    batch_start: int,
) -> QuizPromptResponse:
    has_url = bool(source_url and source_url.strip())
    has_text = bool(source_text and source_text.strip())

    if not has_url and not has_text:
        raise HTTPException(status_code=400, detail="Provide either a source URL or pasted source text.")

    payload = None
    source_label = ""
    source_content = ""
    source_title = topic_override.strip() if topic_override and topic_override.strip() else ""

    if has_url:
        payload = _extract_page_payload(source_url.strip())
        source_label = f"URL: {source_url.strip()}"
        source_content = _render_source_excerpt(payload, source_text or "")
        if not source_title:
            source_title = _pick_topic_title(payload, topic_override, subject, source_url.strip())
    else:
        source_label = f"Text input for {subject}"
        source_content = (source_text or "").strip()
        source_title = source_title or f"{subject.title()} Topic"

    if not source_title:
        source_title = f"{subject.title()} Topic"

    prompt_markdown = _build_quiz_prompt_text(source_label, source_content, subject, source_title, batch_start)
    filename = f"quiz_{_slugify(source_title)}.md"
    return QuizPromptResponse(
        source_label=source_label,
        source_title=source_title,
        batch_range=f"{batch_start}-{batch_start + 9}",
        filename=filename,
        prompt_markdown=prompt_markdown,
    )


def build_study_guide_markdown(url: str, subject: str, topic_override: Optional[str]) -> StudyGuideResponse:
    payload = _extract_page_payload(url)
    topic_title = _pick_topic_title(payload, topic_override, subject, url)
    key_phrases = _pick_key_phrases(payload, limit=18)
    headings = payload["headings"] or [topic_title, "Core Concepts", "Common Pitfalls"]
    code_samples = payload["code_samples"]

    summary = [
        f"This guide covers **{topic_title}** and distills the source page into exam-ready notes anchored to the page structure and wording.",
        "It organizes the material into major themes, the mechanism behind them, and the terminology that is most likely to matter under time pressure.",
        "Use it to review the structure first, then test yourself with the recall questions before trying to explain the topic from memory.",
    ]

    pillar_titles = []
    for heading in headings:
        if heading and heading not in pillar_titles:
            pillar_titles.append(heading)
        if len(pillar_titles) == 8:
            break
    fallback_pillars = [
        "Purpose and scope",
        "Core mechanism",
        "Syntax and structure",
        "Inputs and outputs",
        "Rules and constraints",
        "Common mistakes",
        "Best-practice workflow",
        "Review checklist",
    ]
    while len(pillar_titles) < 6:
        pillar_titles.append(fallback_pillars[len(pillar_titles) % len(fallback_pillars)])

    lines: List[str] = []
    lines.append(f"# 📚 {topic_title} — Exam Study Guide")
    lines.append(f"Source: [{url}]({url})")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    for sentence in summary:
        lines.append(sentence)
    lines.append("")
    lines.append("## Core Pillars")
    lines.append("")
    for idx, pillar in enumerate(pillar_titles[:8], start=1):
        lines.append(f"### {idx}. {pillar}")
        supporting = key_phrases[(idx - 1) * 2 : (idx - 1) * 2 + 2]
        if supporting:
            for phrase in supporting:
                lines.append(f"- **{phrase}** appears in the source and deserves deliberate review.")
        else:
            lines.append("- Keep the main rule or concept in focus when reviewing this section.")

        if code_samples and idx == 1:
            language = _detect_code_language(code_samples[0])
            lines.append(f"```{language}")
            lines.append(code_samples[0].strip()[:1000] or "// sample code from source")
            lines.append("```")
        elif idx == 2 and len(code_samples) > 1:
            language = _detect_code_language(code_samples[1])
            lines.append(f"```{language}")
            lines.append(code_samples[1].strip()[:1000] or "<!-- sample code from source -->")
            lines.append("```")
        lines.append("")

    deep_dive_heading = pillar_titles[0] if pillar_titles else topic_title
    lines.append("## Technical Deep-Dive")
    lines.append("")
    lines.append(f"### Step-by-Step Logic Walkthrough: {deep_dive_heading}")
    lines.append("")
    lines.append("1. **Input** — Identify the problem statement, page rule, or example pattern the source is trying to explain.")
    lines.append("2. **Process** — Map the visible structure, the key attributes, or the sequence of operations that the page emphasizes.")
    lines.append("3. **Output** — Confirm the final behavior, rendered result, or response that should appear when the mechanism is used correctly.")
    if code_samples:
        language = _detect_code_language(code_samples[-1])
        lines.append("")
        lines.append(f"```{language}")
        lines.append(code_samples[-1].strip()[:1000] or "// representative example")
        lines.append("```")
    lines.append("")

    lines.append("## Key Terminology Bank")
    lines.append("")
    lines.append("| Term | Meaning |")
    lines.append("|---|---|")
    term_pool = []
    for phrase in key_phrases:
        cleaned = phrase.strip()
        if cleaned and cleaned not in term_pool:
            term_pool.append(cleaned)
    while len(term_pool) < 15:
        term_pool.append(f"Core idea {len(term_pool) + 1}")
    for term in term_pool[:15]:
        lines.append(f"| **`{term}`** | Important source concept to remember during recall. |")
    lines.append("")

    lines.append("## Watch Out For...")
    lines.append("")
    traps = [
        ("Surface reading", "Assuming the first visible heading is the whole topic", "Read the page structure, code, and supporting text together."),
        ("Context loss", "Treating a rule as universal when it only applies in one example", "Check whether the source limits the rule to a specific case."),
        ("Ignoring examples", "Skipping code blocks because the prose seems sufficient", "Code blocks usually carry the operational detail."),
        ("Overgeneralizing", "Using one section to explain the entire page", "Separate the main pattern from the edge cases and exceptions."),
        ("Missing constraints", "Thinking an implementation works even if a required attribute or step is omitted", "Constraints are part of the answer, not an optional detail."),
        ("Wrong priority", "Putting memorization ahead of mechanism", "Learn the mechanism first so the details make sense."),
        ("Terminology drift", "Using similar words as if they mean the same thing", "Use the page's exact language when possible."),
        ("No review pass", "Assuming the first draft is enough for exam prep", "Use the recall questions and tighten weak spots before saving."),
    ]
    for name, wrong, truth in traps:
        lines.append(f"- **{name}** — {wrong} — {truth}")
    lines.append("")

    lines.append("## Active Recall")
    lines.append("")
    questions = [
        ("Conceptual", f"What is the core purpose of **{topic_title}** in the source material?"),
        ("Code", "Which example code or structure from the page best demonstrates the main mechanism?"),
        ("Contrast", "What changes when you compare the simplest path with the more complete or safer path?"),
        ("Prediction", "If one key rule is removed, what outcome should you expect and why?"),
        ("Integration", "How would you explain the topic to someone else using the page's vocabulary and examples?"),
    ]
    for idx, (kind, prompt) in enumerate(questions, start=1):
        lines.append(f"{idx}. **{kind}** — {prompt}")
    lines.append("")

    lines.append("## Answer Key")
    lines.append("")
    for idx, (kind, prompt) in enumerate(questions, start=1):
        lines.append(f"### {idx}. {kind}")
        lines.append(f"Full marks answer: The source frames **{topic_title}** around the page's main headings, examples, and constraints, so a strong answer should describe the mechanism, mention at least one concrete example, and explain why the rule matters in practice.")
        lines.append("")

    markdown = "\n".join(lines).strip() + "\n"
    filename = f"{_slugify(subject)}_{_slugify(topic_title)}_study_guide.md"
    return StudyGuideResponse(
        source_url=url,
        source_title=topic_title,
        filename=filename,
        markdown=markdown,
    )


def parse_quiz_markdown(markdown_text: str) -> List[QuizQuestion]:
    content = _normalize_newlines(markdown_text).strip()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded markdown file is empty.")

    blocks = [b.strip() for b in SPLIT_QUESTIONS_RE.split(content) if b.strip()]
    questions: List[QuizQuestion] = []

    for index, block in enumerate(blocks, start=1):
        header_match = QUESTION_HEADER_RE.search(block)
        if not header_match:
            raise HTTPException(
                status_code=400,
                detail=f"Question block {index} is missing a valid header: ### Question [Number]: [Title]",
            )

        number = int(header_match.group(1))
        title = header_match.group(2).strip()

        hint_match = HINT_RE.search(block)
        if not hint_match:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Question {number}: missing hint block. Expected: "
                    "<details><summary><b>Hint</b></summary>...</details>."
                ),
            )

        # Only parse options before the hint block so rationale bullets are not treated as choices.
        option_section = block[: hint_match.start()]
        option_starts = list(OPTION_START_RE.finditer(option_section))
        option_count = len(option_starts)
        if option_count not in (2, 4):
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Question {number}: expected either 2 options (- A), - B)) "
                    "or 4 options (- A), - B), - C), - D))."
                ),
            )

        option_letters = [m.group(1).upper() for m in option_starts]
        expected_letters = ["A", "B"] if option_count == 2 else ["A", "B", "C", "D"]
        if option_letters != expected_letters:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Question {number}: options must be in order: "
                    f"{', '.join(expected_letters)}."
                ),
            )

        options: List[QuizOption] = []
        for idx, start_match in enumerate(option_starts):
            next_start = option_starts[idx + 1].start() if idx + 1 < option_count else len(option_section)
            inline_text = start_match.group(2).strip()
            continuation = option_section[start_match.end() : next_start].strip("\n")
            option_text = inline_text
            if continuation.strip():
                option_text = f"{option_text}\n{continuation}" if option_text else continuation

            options.append(
                QuizOption(letter=start_match.group(1).upper(), text=option_text.strip())
            )

        body_start = header_match.end()
        body_end = option_starts[0].start()
        body_markdown = block[body_start:body_end].strip()
        hint_markdown = hint_match.group(1).strip()

        answer_block_match = ANSWER_BLOCK_RE.search(block)
        if not answer_block_match:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Question {number}: missing answer block. Expected: "
                    "<details><summary><b>View Answer & Detailed Rationale</b></summary>...</details>."
                ),
            )

        answer_block_content = answer_block_match.group(1)

        correct_answer_match = CORRECT_ANSWER_RE.search(answer_block_content)
        if not correct_answer_match:
            raise HTTPException(
                status_code=400,
                detail=f"Question {number}: missing '**Correct Answer:** [Letter]' in answer block.",
            )
        correct_answer = correct_answer_match.group(1).upper()
        if correct_answer not in option_letters:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Question {number}: correct answer '{correct_answer}' is not present in options "
                    f"({', '.join(option_letters)})."
                ),
            )

        rationale_section_match = RATIONALE_SECTION_RE.search(answer_block_content)
        if not rationale_section_match:
            raise HTTPException(
                status_code=400,
                detail=f"Question {number}: missing '**Rationale:**' section in answer block.",
            )
        rationale_section = rationale_section_match.group(1).strip()

        rationale_points: List[RationalePoint] = []
        lettered_rationales = list(RATIONALE_LETTER_BULLET_RE.finditer(rationale_section))
        if lettered_rationales:
            rationale_points = [
                RationalePoint(letter=m.group(1).upper(), text=m.group(2).strip())
                for m in lettered_rationales
            ]
        else:
            generic_rationales = list(RATIONALE_GENERIC_BULLET_RE.finditer(rationale_section))
            if not generic_rationales:
                raise HTTPException(
                    status_code=400,
                    detail=f"Question {number}: rationale must contain bulleted explanations.",
                )
            rationale_points = [
                RationalePoint(text=m.group(1).strip())
                for m in generic_rationales
            ]

        questions.append(
            QuizQuestion(
                number=number,
                title=title,
                body_markdown=body_markdown,
                options=options,
                hint_markdown=hint_markdown,
                correct_answer=correct_answer,
                rationale=rationale_points,
            )
        )

    if not questions:
        raise HTTPException(status_code=400, detail="No valid questions were found in the markdown file.")

    return questions






@app.get("/")
def serve_index() -> FileResponse:
    index_path = Path(__file__).parent.parent / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found.")
    return FileResponse(index_path)


# Mount static files (externalized CSS)
css_path = Path(__file__).parent.parent / "css"
if css_path.exists():
    app.mount("/css", StaticFiles(directory=str(css_path)), name="css")


@app.post("/api/upload-quiz", response_model=ParsedQuiz)
async def upload_quiz(file: UploadFile = File(...)) -> ParsedQuiz:
    filename = file.filename or "uploaded_quiz.md"
    if not filename.lower().endswith(".md"):
        raise HTTPException(status_code=400, detail="Only .md files are accepted.")

    raw = await file.read()
    try:
        markdown_text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded markdown.") from exc

    questions = parse_quiz_markdown(markdown_text)
    return ParsedQuiz(source_file=filename, question_count=len(questions), questions=questions)


@app.post("/api/generate-study-guide", response_model=StudyGuideResponse)
async def generate_study_guide(request: StudyGuideRequest) -> StudyGuideResponse:
    return build_study_guide_markdown(request.url, request.subject, request.topic)


@app.post("/api/generate-quiz-prompt", response_model=QuizPromptResponse)
async def generate_quiz_prompt(request: QuizPromptRequest) -> QuizPromptResponse:
    if request.batch_start < 1:
        raise HTTPException(status_code=400, detail="Batch start must be 1 or greater.")
    return build_quiz_prompt_markdown(
        request.source_url,
        request.source_text,
        request.subject,
        request.topic,
        request.batch_start,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)