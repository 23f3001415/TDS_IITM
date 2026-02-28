from __future__ import annotations

import os
import re
import sys
import traceback
from io import StringIO
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="GA3 Q3 Code Interpreter")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodeRequest(BaseModel):
    code: str = Field(min_length=1)


class CodeResponse(BaseModel):
    error: List[int]
    result: str


class ErrorAnalysis(BaseModel):
    error_lines: List[int]


def execute_python_code(code: str) -> dict:
    """
    Execute Python code and return exact output.

    Returns:
        {
            "success": bool,
            "output": str  # Exact stdout/stderr or traceback
        }
    """
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = StringIO()
    sys.stderr = StringIO()

    try:
        exec_globals = {"__builtins__": __builtins__}
        exec(code, exec_globals)
        output = sys.stdout.getvalue() + sys.stderr.getvalue()
        return {"success": True, "output": output}
    except Exception:
        # Keep stdout/stderr exactly as produced before the crash.
        output = sys.stdout.getvalue() + sys.stderr.getvalue() + traceback.format_exc()
        return {"success": False, "output": output}
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


def extract_error_lines_from_traceback(tb_text: str) -> List[int]:
    # Prefer user code frames from exec(code), which are usually "<string>".
    matches = re.findall(r'File "<string>", line (\d+)', tb_text)
    if matches:
        return [int(matches[-1])]

    # Fallback for non-standard formatting.
    generic = re.findall(r"\bline (\d+)\b", tb_text)
    if generic:
        return [int(generic[-1])]
    return []


def analyze_error_with_ai(code: str, traceback_text: str) -> List[int]:
    """
    Use Gemini structured output to identify error line numbers.
    Falls back to traceback parsing if Gemini is unavailable.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        return extract_error_lines_from_traceback(traceback_text)

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=gemini_key)
        prompt = f"""
Analyze this Python code and traceback.
Return line number(s) in the USER CODE where the error actually occurred.

CODE:
{code}

TRACEBACK:
{traceback_text}
"""
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "error_lines": types.Schema(
                            type=types.Type.ARRAY,
                            items=types.Schema(type=types.Type.INTEGER),
                        )
                    },
                    required=["error_lines"],
                ),
            ),
        )
        parsed = ErrorAnalysis.model_validate_json(response.text)
        clean = [int(x) for x in parsed.error_lines if int(x) > 0]
        if clean:
            return clean
    except Exception:
        pass

    return extract_error_lines_from_traceback(traceback_text)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/code-interpreter", response_model=CodeResponse)
def code_interpreter(payload: CodeRequest) -> CodeResponse:
    code = payload.code
    if not code.strip():
        raise HTTPException(status_code=400, detail="code must not be empty")

    executed = execute_python_code(code)
    if executed["success"]:
        return CodeResponse(error=[], result=executed["output"])

    error_lines = analyze_error_with_ai(code, executed["output"])
    return CodeResponse(error=error_lines, result=executed["output"])


@app.exception_handler(HTTPException)
def http_exception_handler(_, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=False)
