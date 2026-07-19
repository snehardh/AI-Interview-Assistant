from openai import OpenAI
from dotenv import load_dotenv
import os

from prompts import QUESTION_PROMPT, EVALUATION_PROMPT

# Load environment variables
load_dotenv()

# Create OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Free model (change if needed)
MODEL = "tencent/hy3:free"


def generate_questions(resume, job_description):

    prompt = QUESTION_PROMPT.format(
        resume=resume,
        job_description=job_description
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1000
    )

    text = response.choices[0].message.content

    questions = []

    for line in text.split("\n"):

        line = line.strip()

        if (
            line
            and (
                line[0].isdigit()
                or line.startswith("-")
                or line.startswith("*")
            )
        ):

            line = line.lstrip("0123456789.-* ")

            if line:
                questions.append(line)

    return questions


def evaluate_answer(question, answer):

    prompt = EVALUATION_PROMPT.format(
        question=question,
        answer=answer
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        max_tokens=1000
    )

    return response.choices[0].message.content