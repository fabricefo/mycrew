import os
import warnings
warnings.filterwarnings('ignore')
from crewai import LLM, Agent, Crew, Process, Task  # noqa: E402
from crewai.project import CrewBase, agent, crew, task# noqa: E402
from tools.image_search_tool import pexels_cover_tool  # noqa: E402
from dotenv import load_dotenv  # noqa: E402
load_dotenv()
from slugify import slugify

@CrewBase
class BlogWritingCrew:
    """Blog Writing Crew with only Draft Creator and Senior Writer."""

    agents_config = "blog_agents.yaml"
    tasks_config = "blog_tasks.yaml"

    def __init__(self): 
        self.pexels_cover_tool = pexels_cover_tool
        self.gemini_flash = LLM(
            model="gemini/gemini-2.5-flash",
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.01,
        )

    @agent
    def draft_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["draft_creator"],  # type: ignore
            llm=self.gemini_flash,
            verbose=True,
            allow_delegation=False,
            max_iter=10,
        )

    @agent
    def senior_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_writer"],  # type: ignore
            llm=self.gemini_flash,
            verbose=True,
            allow_delegation=True,
            max_iter=10
        )
    
    @agent
    def designer(self) -> Agent:
        return Agent(
            config=self.agents_config["designer"],  # type: ignore
            tools=[self.pexels_cover_tool],
            llm=self.gemini_flash,
            verbose=True,
            allow_delegation=False,
            max_iter=5
        )   
    
    @agent
    def publisher(self) -> Agent:
        return Agent(
            config=self.agents_config["publisher"],  # type: ignore
            llm=self.gemini_flash, 
            verbose=True,
            allow_delegation=False,
            max_iter=5
        )
    
    @agent
    def social_media_post_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["social_media_post_creator"],  # type: ignore
            llm=self.gemini_flash,
            verbose=True,
            allow_delegation=False,
            max_iter=5
        )

    @task
    def draft_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config["draft_creation_task"],  # type: ignore
            agent=self.draft_creator(),
            markdown=True,
            output_file="output/drafts/draft_creation_{topic}.md",
        )

    @task
    def final_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config["final_writing_task"],  # type: ignore
            agent=self.senior_writer(),
            context=[self.draft_creation_task()],
            markdown=True,
            output_file="output/blogs/final_writing_{topic}.md",
        )
    
    @task
    def publishing_task(self) -> Task:
        return Task(
            config=self.tasks_config["publishing_task"],  # type: ignore
            agent=self.publisher(),
            context=[self.final_writing_task()],
            output_file="output/publication/{topic}.md",
        )
    
    @task
    def social_media_post_task(self) -> Task:
        return Task(
            config=self.tasks_config["social_media_post_task"],  # type: ignore
            agent=self.social_media_post_creator(),
            context=[self.draft_creation_task(),self.publishing_task()],
            output_file="output/social_media/linkedin_post_{topic}.txt",
        )
    
    @task
    def design_image_task(self) -> Task:
        return Task(
            config=self.tasks_config["design_image_task"],  # type: ignore
            agent=self.designer(),
            context=[self.final_writing_task()],
            output_file="output/images/cover_image_{topic}.jpg",
        )


    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # type: ignore
            tasks=self.tasks,  # type: ignore
            process=Process.sequential,
            verbose=True,
            memory=False,
            max_rpm=40,            
            language="en",  # type: ignore
        )
 