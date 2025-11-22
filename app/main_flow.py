from typing import Dict, Any
from crewai.flow.flow import Flow, listen, start
from crews.blog_crew.blog_crew import BlogWritingCrew
from dotenv import load_dotenv

load_dotenv()

class BlogWritingFlow(Flow):
    """
    Flow for automated blog writing with separated research and content creation crews.
    """
    def __init__(self, topic: str = None, word_count: str = None, read_time: str = None):
        super().__init__()
        # Store inputs as instance variables
        self.topic = topic or "La difference entre Pulumi et Terraform"
        self.word_count = word_count or "1200"
        self.read_time = read_time or "8"
        self.blog_crew = BlogWritingCrew()

    @start()
    def initiate_blog_creation(self) -> Dict[str, Any]:
        """
        Initialize flow with stored user inputs.
        """
        inputs = {
            "topic": self.topic,
            "word_count": self.word_count,
            "read_time": self.read_time
        }
        print(f"🚀 Starting blog creation flow for: {inputs['topic']}")
        return inputs

    @listen(initiate_blog_creation)
    def content_creation_phase(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 1: Create content, publish, and generate social media post.
        """
        print(f"✍️ Phase 1: Content Creation, Publishing & Social Media for '{inputs['topic']}'")
        # Execute blog writing crew
        blog_result = self.blog_crew.crew().kickoff(inputs=inputs)
        print("✅ Content creation phase completed!")
        return {
            **inputs,
            "content_completed": True,
            "blog_result": str(blog_result),
            "final_output": str(blog_result)
        }

# Create flow instance for import
blog_writing_flow = BlogWritingFlow()