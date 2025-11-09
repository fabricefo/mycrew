import os
from crewai import Agent, Task, Crew, Process

# Charger .env si python-dotenv est installé (optionnel)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv absent ou échec de chargement -> continuer, on utilisera les variables d'environnement
    pass

# Optional: Use environment variables for API keys
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL="gpt-4o-mini"

def create_crew():
    # Define agents
    researcher = Agent(
        role='Researcher',
        goal='Conduct thorough research on {topic}',
        verbose=True,
        memory=True,
        backstory='A diligent researcher passionate about uncovering insights.',
    )

    writer = Agent(
        role='Writer',
        goal='Write a compelling article about {topic}',
        verbose=True,
        memory=True,
        backstory='A creative writer who simplifies complex topics.',
    )

    # Define tasks
    research_task = Task(
        description=(
            "Research the topic and gather key points."
            "Your report should include the pros and cons."
        ),
        expected_output='A detailed summary of the topic.',
        agent=researcher,
    )

    write_task = Task(
        description=(
            "Write an article based on the research."
            "Make it engaging and informative."
        ),
        expected_output='A 500-word article in markdown format.',
        agent=writer,
    )

    # Define crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
    )

    return crew

def kickoff_crew(inputs):
    crew = create_crew()
    return crew.kickoff(inputs=inputs)