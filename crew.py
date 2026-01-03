import os
from crewai import Agent, Task, Crew, Process, LLM
from tools import SearchTool, FileSaveTool

# --- CONFIGURE THE BRAIN ---
# We are using the newer Gemini 2.5 Flash model available in your region
my_key = os.environ.get("GEMINI_API_KEY")
if my_key:
    my_key = my_key.strip() # Safety trim

llm = LLM(
    model="gemini/gemini-2.0-flash-lite",
    api_key=my_key
)

def kickoff_support_crew(inputs):
    # Instantiate Tools
    search_tool = SearchTool()
    file_tool = FileSaveTool()

    # --- AGENTS ---
    
    # Agent 1: Researcher
    researcher = Agent(
        role='Knowledge Base Researcher',
        goal='Search existing documentation for related solutions.',
        backstory='You are an expert researcher who checks the internet for similar past issues.',
        tools=[search_tool],
        llm=llm,
        verbose=True
    )

    # Agent 2: Specialist
    specialist = Agent(
        role='Technical Support Specialist',
        goal='Analyze the issue and provide a step-by-step solution.',
        backstory='You are a senior engineer. You analyze the research and the ticket details to propose a safe fix.',
        llm=llm,
        verbose=True
    )

    # Agent 3: Documentation Writer
    doc_writer = Agent(
        role='Documentation Writer',
        goal='Create documentation and save it.',
        backstory='You take the solution and format it into a professional help article, then save it.',
        tools=[file_tool],
        llm=llm,
        verbose=True
    )

    # --- TASKS ---

    task_research = Task(
        description=f"Research this issue: {inputs['ticket_issue']}. Priority: {inputs['ticket_priority']}.",
        expected_output='A summary of similar issues and potential fixes found online.',
        agent=researcher
    )

    task_resolve = Task(
        description=f"Using the research, solve this ticket for customer {inputs['customer_name']}. Details: {inputs['ticket_details']}",
        expected_output='A detailed step-by-step technical solution.',
        agent=specialist
    )

    task_document = Task(
        description='Create a "Knowledge Base Article" from the solution and save it to the file using the tool.',
        expected_output='Confirmation that the file was saved.',
        agent=doc_writer
    )

    # --- CREW ---
    crew = Crew(
        agents=[researcher, specialist, doc_writer],
        tasks=[task_research, task_resolve, task_document],
        process=Process.sequential
    )

    return crew.kickoff()