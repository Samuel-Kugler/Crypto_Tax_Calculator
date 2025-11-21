from fastapi import FastAPI

#uvicorn app.main:app --reload
app = FastAPI()

@app.get("/")
def works():
    return {"status": "ok"}
