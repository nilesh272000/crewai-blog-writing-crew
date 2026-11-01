import os
from dotenv import load_dotenv

load_dotenv()


def is_mock_mode() -> bool:
    return os.getenv("MOCK_MODE", "false").lower() == "true"


def llm_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def default_target_words() -> int:
    return int(os.getenv("DEFAULT_TARGET_WORDS", "1200"))
