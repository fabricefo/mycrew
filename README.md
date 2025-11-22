# My Crew

Welcome to the My Crew project, powered by [crewAI](https://crewai.com). .

This project is in progress, the main goal is to create a crew of assistants for me :)
The crew will be connected to my Telegram bot with the help of n8n to manage the triggers and conversation.

Original source : https://github.com/vishvaRam/Blog-Writing-Agentic-RAG-CrewAI

## Project setup

1. Install uv : ```pip install uv```
2. Install CrewAI : ```crewai install```
3. Install FastAPI : ```uv add fastapi --extra standard```

Test with command line : 
- with : ```uv run fastapi dev app/main.py```
- Open https://localhost:8000/docs
- Try out the endpoint /kickoff with {{"topic":"Anything you want..."}} as a json input.

Test with Docker : 
- Build the Docker image with: ```docker build -t --build-arg OPENAI_API_KEY="********" mycrew-app .```
- Run the Docker container locally with: ```docker run -p 8000:8000 mycrew-app```
- Open https://localhost:8000/docs
- Try out the endpoint /kickoff with {{"topic":"Anything you want..."}} as a json input.

## TODO

- Create agents for personal usage : mail/calendar, travel, content management, finance
- Build full API for purposes
- Finalize Github workflows with deployment to server
- Integrate into n8n and connect to Telegram bot