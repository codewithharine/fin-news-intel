from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Financial News Intelligence System Running 🚀"}
