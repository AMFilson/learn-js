from __future__ import annotations

from collections import Counter
import html as html_module
import os
import re
from pathlib import Path
from typing import List, Optional
from urllib.error import URLError, HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import google.generativeai as genai

# Setup Gemini API (Make sure GOOGLE_API_KEY is in Vercel Env Vars)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


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


QUESTION_HEADER_RE = re.compile(r"^###\s+Question\s+(\d+)\s*[:.]?\s*(.+)$", re.MULTILINE)
OPTION_START_RE = re.compile(r"^\s*-\s*([A-D])[\).:]\s*(.*)$", re.MULTILINE)
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
RATIONALE_LETTER_BULLET_RE = re.compile(r"^\s*-\s*([A-D])[\).:]\s+(.+?)\s*$", re.MULTILINE)
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
    value = value.replace("\u00a0", " ") # Handle non-breaking spaces
    value = SCRIPT_STYLE_RE.sub("", value) # Strip scripts and styles
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


STUDY_GUIDE_SYSTEM_PROMPT = """You are an expert technical writer and educator. Your task is to synthesize the provided web page content into a comprehensive, exam-ready Markdown study guide.

You MUST follow this exact document structure:

# 📚 [Topic Title] — Exam Study Guide
Source: [URL]

## Executive Summary
[Exactly 3 sentences: (1) what the page is about, (2) the central concept/mechanism, (3) the most important exam-critical takeaway.]

## Core Pillars
[Create 6-12 pillars. Each pillar must use an `### [Number]. [Title]` heading. Prefer bullet points over paragraphs. Include any important code examples from the source in fenced code blocks.]

## Technical Deep-Dive
[Provide a step-by-step logic walkthrough of the most complex mechanism. Include a setup, step-by-step narration, and output.]

## Key Terminology Bank
[Create a Markdown table with `| Term | Exam-Ready Definition |`. Include at least 15 terms found in the source.]

## Watch Out For...
[List at least 8 bullet points covering common misconceptions, default values, limitations, or traps. Format: `1. **[Trap Name]** — [Incorrect Assumption] — [Truth]`]

## Active Recall — Check for Understanding
[Provide exactly 5 questions: (1) Conceptual, (2) Code, (3) Contrast, (4) Prediction, (5) Integration.]

## Answer Key
[Provide full, comprehensive answers to the 5 Active Recall questions above.]

Tone: Professional, concise, logically dense, no filler fluff. Bold critical keywords. NEVER deviate from this exact markdown heading structure.
"""


def build_study_guide_markdown(url: str, subject: str, topic_override: Optional[str]) -> StudyGuideResponse:
    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY environment variable is not configured.")

    payload = _extract_page_payload(url)
    topic_title = _pick_topic_title(payload, topic_override, subject, url)
    content_excerpt = _render_source_excerpt(payload, "", limit_chars=35000)

    try:
        # Based on check_models.py, the correct string for Gemini 3.1 Flash Lite is 'gemini-3.1-flash-lite-preview'
        model = genai.GenerativeModel("gemini-3.1-flash-lite-preview", system_instruction=STUDY_GUIDE_SYSTEM_PROMPT)
        prompt = f"Target Subject: {subject}\nTopic Override: {topic_title}\nSource URL: {url}\n\nCONTENT TO SYNTHESIZE:\n{content_excerpt}"
        
        response = model.generate_content(prompt)
        markdown = response.text.replace("```markdown", "").replace("```", "").strip() + "\n"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {e}")

    filename = f"{_slugify(subject)}_{_slugify(topic_title)}_study_guide.md"
    return StudyGuideResponse(
        source_url=url,
        source_title=topic_title,
        filename=filename,
        markdown=markdown,
    )


QUIZ_SYSTEM_PROMPT = """You are TestFlow's Quiz Architect. Your task is to generate a high-depth practice quiz from the provided documentation.

You must generate EXACTLY 10 questions.
For EVERY question, you MUST follow this EXACT sequence and formatting natively:

### Question [Number]: [Topic]
[Scenario / Problem Description]

- A) [Option]
- B) [Option]
- C) [Option]
- D) [Option]

<details>
<summary><b>Hint</b></summary>
[Provide a conceptual nudge without giving it away.]
</details>

<details>
<summary><b>View Answer & Detailed Rationale</b></summary>

**Correct Answer:** [Letter]

**Rationale:**
- **Why [Correct Letter] is optimal:** [2-3 sentences of deep technical explanation.]
- **Why [Incorrect Letter 1] is wrong:** [2-3 sentences explaining the technical violation.]
- **Why [Incorrect Letter 2] is wrong:** [2-3 sentences explaining why it's suboptimal.]
- **Why [Incorrect Letter 3] is wrong:** [2-3 sentences explaining why it fails.]
</details>

---

CRITICAL RULES:
- There must be a blank line between `</details>` and `---`.
- There must be a blank line after the `<summary>` tags inside the `<details>` blocks before the actual content to ensure markdown parses correctly.
- NEVER invent HTML attributes or functions that do not exist in the source context.
- Your output must consist ONLY of the questions in this format, starting with `### Question 1:`.
"""

def generate_ai_quiz(url: Optional[str], subject: str, topic_override: Optional[str], exclude_titles: List[str] = [], source_text: Optional[str] = None) -> ParsedQuiz:
    if not GOOGLE_API_KEY:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY is not configured.")

    if source_text:
        topic_title = topic_override or f"{subject.title()} Study Guide"
        content_excerpt = source_text[:30000]
    else:
        if not url:
            raise HTTPException(status_code=400, detail="Either URL or source text must be provided.")
        payload = _extract_page_payload(url)
        topic_title = _pick_topic_title(payload, topic_override, subject, url)
        content_excerpt = _render_source_excerpt(payload, "", limit_chars=30000)

    try:
        # Based on check_models.py, the correct string for Gemini 3.1 Flash Lite is 'gemini-3.1-flash-lite-preview'
        model = genai.GenerativeModel("gemini-3.1-flash-lite-preview", system_instruction=QUIZ_SYSTEM_PROMPT)
        
        exclude_clause = ""
        if exclude_titles:
            exclude_clause = f"\n\nCRITICAL CONSTRAINT: DO NOT generate questions that are identical or very similar to these previously used titles:\n- " + "\n- ".join(exclude_titles)

        prompt = f"Please generate a 10-question technical quiz specifically about this content focusing on {topic_title}:{exclude_clause}\n\n{content_excerpt}"
        
        response = model.generate_content(prompt)
        markdown_output = response.text.strip()
        
        # We run the LLM output through our own strict parser to guarantee the structure
        questions = parse_quiz_markdown(markdown_output)
        
    except HTTPException as e:
        # Re-raise parsing failures so the frontend gets them 
        raise e 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API or Parsing Error: {e}")

    filename = f"quiz_{_slugify(topic_title)}.md"
    return ParsedQuiz(
        source_file=filename,
        question_count=len(questions),
        questions=questions
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






@app.get("/favicon.ico", include_in_schema=False)
@app.get("/icon.ico", include_in_schema=False)
async def serve_favicon():
    icon_path = Path(__file__).parent.parent / "images" / "icon.ico"
    if not icon_path.exists():
        raise HTTPException(status_code=404, detail="Icon not found.")
    return FileResponse(icon_path)


@app.get("/")
def serve_index() -> FileResponse:
    index_path = Path(__file__).parent.parent / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found.")
    return FileResponse(index_path)


# Mount static files (Externalized CSS and Images)
css_path = Path(__file__).parent.parent / "css"
if css_path.exists():
    app.mount("/css", StaticFiles(directory=str(css_path)), name="css")

images_path = Path(__file__).parent.parent / "images"
if images_path.exists():
    app.mount("/images", StaticFiles(directory=str(images_path)), name="images")


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
    # Use the real AI logic instead of mock templates.
    return build_study_guide_markdown(request.url, request.subject, request.topic)


@app.post("/api/build-quiz-from-url", response_model=ParsedQuiz)
async def build_quiz_from_url(
    url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    subject: str = Form("General"),
    topic: Optional[str] = Form(None),
    exclude_titles: str = Form("[]")
) -> ParsedQuiz:
    source_text = None
    if file:
        raw = await file.read()
        source_text = raw.decode("utf-8", errors="ignore")
    
    try:
        excludes = json.loads(exclude_titles)
    except:
        excludes = []

    return generate_ai_quiz(url, subject, topic, excludes, source_text=source_text)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)