import os
import sys
from fastapi import FastAPI
import openai
from dotenv import load_dotenv

from src.db.models import ProblemBase

load_dotenv()

app = FastAPI()

openai.api_key = os.environ.get("OPENAI_API_KEY")


async def get_response(message):
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        
        messages=[
            {"role": "user", "content": "こんにちは、あなたにできることを教えてください。"},
        ],
    )
    return res.choices[0].text.strip()

def receive_signal(signalNumber, frame):
    print('Received:', signalNumber)
    sys.exit()


@app.on_event("startup")
async def startup_event():
    import signal
    signal.signal(signal.SIGINT, receive_signal)


@app.get("/")
async def root():
    return {"message": "This is the root of the API of the edu-pl project."}


@app.get("/problems/{problem_id}")
async def get_problem(problem_id: int):
    return {"problem_id": problem_id}


@app.get("/hello_test")
async def hello_test():
    res = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a teacher. You will now be asked a question by a student, so please respond in Japanese."},
            {"role": "user", "content": "こんにちは、あなたにできることを教えてください。"},
        ],
    )       
    return {"response": res.choices[0]["message"]["content"].strip()}

@app.post("/problems")
async def answer_problem(problem: ProblemBase):
    messages = [{"role": "system", "content": "You are a teacher. You will now be asked a question by a student, so please respond in Japanese."}]

    for message in problem.messages:
        messages.append(message.dict())

    res = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages= messages,
    )
    return {"assistant": res.choices[0]["message"]["content"].strip()}
