QUESTION_PROMPT = """
You are an expert technical interviewer.

Resume:
{resume}

Job Description:
{job_description}

Generate exactly 10 interview questions.

Rules:
- Mix HR and Technical questions.
- Ask questions based on the resume.
- Ask questions based on the job description.
- Return only numbered questions.
"""

EVALUATION_PROMPT = """
You are an expert interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Give:

Score: /10

Strengths:
- ...

Weaknesses:
- ...

Suggested Answer:
...
"""