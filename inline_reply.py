import subprocess
import sys
from pathlib import Path
import textwrap


# =========================
# CONFIG (EDIT IF NEEDED)
# =========================

PROJECT_ROOT = Path(__file__).resolve().parent
LLAMA_BIN = PROJECT_ROOT / "llama" / "llama-run.exe"
MODEL_PATH = PROJECT_ROOT / "models" / "tinyllama-1.1b-chat-v1.0.Q8_0.gguf"

MAX_TOKENS = 256
TIMEOUT_SEC = 180


# =========================
# LOW-LEVEL LLM CALL
# =========================

def call_llm(prompt: str, tokens: int = MAX_TOKENS) -> str:
    """
    Runs llama-run.exe once and returns stdout safely.
    """

    cmd = [
        str(LLAMA_BIN),
        str(MODEL_PATH),
        prompt
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=TIMEOUT_SEC
        )
    except subprocess.TimeoutExpired:
        return "[ERROR] LLM timed out."

    if result.stderr.strip():
        return f"[LLM ERROR]\n{result.stderr.strip()}"

    return result.stdout.strip()


# =========================
# INLINE UX LOOP
# =========================

def inline_loop(initial_prompt: str):
    """
    Interactive inline-reply loop (terminal-based).
    """

    current_prompt = initial_prompt

    while True:
        print("\n🧠 Asking local LLM...\n")
        output = call_llm(current_prompt)

        print("\n" + "=" * 60)
        print("AI OUTPUT:\n")
        print(textwrap.fill(output, width=90))
        print("=" * 60)

        print(
            "\nActions:\n"
            "1️⃣ Reply to this\n"
            "2️⃣ Explain this\n"
            "3️⃣ Regenerate\n"
            "0️⃣ Exit\n"
        )

        choice = input("Choose action: ").strip()

        if choice == "0":
            print("👋 Exiting.")
            break

        elif choice == "1":
            reply = input("\nYour reply: ").strip()
            current_prompt = (
                "The following response is incorrect or incomplete:\n\n"
                f"{output}\n\n"
                f"User correction:\n{reply}\n\n"
                "Please respond accurately."
            )

        elif choice == "2":
            current_prompt = (
                "Explain the following response clearly and correctly:\n\n"
                f"{output}"
            )

        elif choice == "3":
            current_prompt = initial_prompt

        else:
            print("❌ Invalid option. Try again.")


# =========================
# ENTRY POINT (SAFE)
# =========================

if __name__ == "__main__":
    if not LLAMA_BIN.exists():
        print("❌ llama-run.exe not found.")
        sys.exit(1)

    if not MODEL_PATH.exists():
        print("❌ Model file not found.")
        sys.exit(1)

    inline_loop("Explain what SGIN (Sleeping GPU Inference Network) is.")
