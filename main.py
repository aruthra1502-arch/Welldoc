import os, json, subprocess, textwrap, sys

# ---- Configure model name for Ollama (already pulled) ----
MODEL = "mistral"

# ---- Minimal spec (you can paste your doc later if needed) ----
SPEC_TEXT = textwrap.dedent("""
You are Agent 1: Developer Agent.

Goal:
Generate a minimal but runnable .NET 8 C# Web API that implements ONE endpoint: CreatePatient.
Follow a 3-layer architecture (Controller, Service, Data). Use EF Core with SQLite. 
Return ONLY a JSON object with the files to create (see Output Format).

Requirements:
- API Name: CreatePatient
- Method: POST /api/patient/create
- Request JSON: { "PatientFirstName": "John", "PatientLastName": "Doe" }
- Response JSON: { "PatientID": 1 }
- DB schema (table Patient):
  - PatientID BIGINT (PK, auto)
  - PatientFirstName NVARCHAR(200) NOT NULL
  - PatientLastName  NVARCHAR(200) NOT NULL
  - RegistrationDatetime DATETIME NOT NULL (UTC Now on insert)
- Layers:
  - Data: DbContext + Entity
  - Service: IPatientService + PatientService
  - Controller: PatientController with Create endpoint
- Project: .NET 8, EF Core Sqlite
- Keep code concise and production-safe basics (nullables enabled, input validation).
- Do NOT include Swagger or extra features.

Output Format (IMPORTANT):
Return strict JSON with this shape, no prose around it:
{
  "files": [
    {"path": "Welldoc.Api/Welldoc.Api.csproj", "content": "<xml>...</xml>"},
    {"path": "Welldoc.Api/Program.cs", "content": "// csharp ..."},
    ...
  ]
}
""").strip()

REVIEW_PROMPT = textwrap.dedent("""
You are Agent 2: Code Review Agent.

Review the provided C# .NET code for a CreatePatient API against 4 areas:
1) Code Quality: naming, meaningful identifiers, method focus, comments (not redundant), exception handling.
2) Best Practices: SOLID/DRY, validation, error handling patterns, async use.
3) Architecture: 3-layer separation (Controller, Service, Data), responsibilities in right layer, DTOs.
4) Security: treatment of PII (patient names), cryptographic practices, input validation, logging of sensitive data.

Return a clear, structured report with headings and bullet points, plus a short "Pass/Blocker" verdict at the end.
""").strip()

def run_ollama(prompt: str, input_text: str = "") -> str:
    proc = subprocess.run(
        ["ollama", "run", MODEL],
        input=(prompt + ("\n\n" + input_text if input_text else "")).encode("utf-8"),
        capture_output=True
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr.decode("utf-8", errors="ignore"))
        raise RuntimeError("ollama run failed")
    return proc.stdout.decode("utf-8", errors="ignore").strip()

def agent1_generate_files():
    raw = run_ollama(SPEC_TEXT)
    # Try to find the first JSON blob in case the model adds stray text
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Model did not return JSON")
    raw_json = raw[start:end+1]
    data = json.loads(raw_json)

    outroot = os.path.join("out", "code")
    os.makedirs(outroot, exist_ok=True)

    generated = []
    for f in data.get("files", []):
        path = f["path"]
        content = f["content"]
        full = os.path.join(outroot, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8", newline="") as fh:
            fh.write(content)
        generated.append(full)
    return generated

def agent2_review_files(paths):
    concatenated = []
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as fh:
                concatenated.append(f"\n\n// FILE: {p}\n" + fh.read())
        except Exception as e:
            concatenated.append(f"\n\n// FILE: {p}\n// ERROR READING: {e}")
    code_blob = "\n".join(concatenated)

    review = run_ollama(REVIEW_PROMPT, code_blob)
    os.makedirs("out", exist_ok=True)
    with open(os.path.join("out", "CodeReviewReport.txt"), "w", encoding="utf-8") as fh:
        fh.write(review)
    return review

if __name__ == "__main__":
    print("Agent 1: Generating C# project…")
    files = agent1_generate_files()
    print(f"Generated {len(files)} files under out/code/")
    print("Agent 2: Reviewing generated code…")
    agent2_review_files(files)
    print("Review saved to out/CodeReviewReport.txt")
    print("\nDone.")
