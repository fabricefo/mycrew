from fastapi import FastAPI
from main_flow import BlogWritingFlow

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
    flow = BlogWritingFlow(topic=inputs.topic, word_count=inputs.word_count, read_time=inputs.read_time)
    result = flow.kickoff()
    return {"result": result}