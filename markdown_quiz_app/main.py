from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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


app = FastAPI(title="Markdown Quiz Parser", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


QUESTION_HEADER_RE = re.compile(r"^###\s+Question\s+(\d+)\s*:\s*(.+)$", re.MULTILINE)
OPTION_RE = re.compile(r"^\s*-\s*([A-D])\)\s+(.+?)\s*$", re.MULTILINE)
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


def _normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


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

        option_matches = list(OPTION_RE.finditer(block))
        if len(option_matches) < 4:
            raise HTTPException(
                status_code=400,
                detail=f"Question {number}: expected 4 options formatted as - A), - B), - C), - D).",
            )

        option_letters = [m.group(1).upper() for m in option_matches]
        expected_letters = ["A", "B", "C", "D"]
        if option_letters[:4] != expected_letters:
            raise HTTPException(
                status_code=400,
                detail=f"Question {number}: options must start in order: A, B, C, D.",
            )

        options = [
            QuizOption(letter=m.group(1).upper(), text=m.group(2).strip())
            for m in option_matches[:4]
        ]

        body_start = header_match.end()
        body_end = option_matches[0].start()
        body_markdown = block[body_start:body_end].strip()

        hint_match = HINT_RE.search(block)
        if not hint_match:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Question {number}: missing hint block. Expected: "
                    "<details><summary><b>Hint</b></summary>...</details>."
                ),
            )
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
    index_path = Path(__file__).parent / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found.")
    return FileResponse(index_path)


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)