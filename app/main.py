from fastapi import FastAPI
from crews.crew_manager import kickoff_crew

app = FastAPI()

@app.get("/help")
async def help_endpoint():
    return {
        "endpoints": {
            "/help": "Get help information about the API.",
            "/kickoff/": "Kickoff the crew with provided inputs."
        }
    }

@app.post("/kickoff/")
async def kickoff_crew_endpoint(inputs: dict):
    result = kickoff_crew(inputs)
    return {"result": result}