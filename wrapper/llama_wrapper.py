import subprocess
import os

LLAMA_RUN = os.path.abspath(
    r"llama-b7640-bin-win-cpu-x64\llama-run.exe"
)

MODEL_PATH = os.path.abspath(
    r"local_llm\models\tinyllama-1.1b-chat-v1.0.Q8_0.gguf"
)

def ask_llm(prompt: str, tokens: int = 128) -> str:
    if not os.path.exists(LLAMA_RUN):
        raise FileNotFoundError(f"llama-run.exe not found: {LLAMA_RUN}")

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    cmd = [
        LLAMA_RUN,
        "-n", str(tokens),
        MODEL_PATH,
        prompt
    ]

    print("🧠 Asking local LLM...\n")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    return result.stdout.strip()


if __name__ == "__main__":
    reply = ask_llm("Hello. Who are you?")
    print("LLM RESPONSE:\n")
    print(reply)
