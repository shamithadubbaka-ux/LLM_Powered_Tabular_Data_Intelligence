import os

from dotenv import load_dotenv


load_dotenv()


APP_TITLE = "LLM-Powered Tabular Data Intelligence"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)

MAX_RESULT_ROWS = 10000