from crewai import Agent, Task, Crew, LLM
import csv


# ---------------------------------------------------------
# 1. Connect CrewAI to your local Ollama model
# ---------------------------------------------------------

llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)


# ---------------------------------------------------------
# 2. Load the incident data
# ---------------------------------------------------------

with open("data/incident_data.csv", newline="", encoding="utf-8") as file:
    incident_data = list(csv.DictReader(file))

data_text = "\n".join(str(row) for row in incident_data)


# ---------------------------------------------------------
# 3. Define the agents
# ---------------------------------------------------------
# Decide what each specialist should do.
# Replace the TODO values.

incident_manager = Agent(
    role="TODO",
    goal="TODO",
    backstory="TODO",
    llm=llm,
    verbose=True
)

log_analyst = Agent(
    role="TODO",
    goal="TODO",
    backstory="TODO",
    llm=llm,
    verbose=True
)

technical_investigator = Agent(
    role="TODO",
    goal="TODO",
    backstory="TODO",
    llm=llm,
    verbose=True
)

root_cause_analyst = Agent(
    role="TODO",
    goal="TODO",
    backstory="TODO",
    llm=llm,
    verbose=True
)

report_generator = Agent(
    role="TODO",
    goal="TODO",
    backstory="TODO",
    llm=llm,
    verbose=True
)


# ---------------------------------------------------------
# 4. Define the tasks
# ---------------------------------------------------------

incident_task = Task(
    description=f"""
    Review the incident data below and create an initial incident overview.

    INCIDENT DATA:
    {data_text}

    TODO: Decide what the Incident Manager should establish first.
    Identify the affected system/component, relevant time period, important
    status changes, and the main areas that require investigation.

    Do not invent information that is not supported by the data.
    """,
    expected_output="TODO: Define the useful output the Incident Manager should provide.",
    agent=incident_manager
)

log_analysis_task = Task(
    description=f"""
    Analyse the incident data below as a data/log specialist.

    INCIDENT DATA:
    {data_text}

    TODO: Decide which anomalies, trends, status changes, error codes,
    timing patterns, or changes before the incident should be identified.
    Support important findings with specific evidence from the data.
    """,
    expected_output="TODO: Define the evidence-focused output expected from the data analysis.",
    agent=log_analyst,
    context=[incident_task],
    async_execution=True
)

technical_task = Task(
    description="""
    Use the incident overview and data analysis to investigate possible
    technical causes of the incident.

    TODO: Decide how this agent should evaluate possible causes, connect
    technical explanations to the evidence, and distinguish evidence from
    assumptions.

    Do not claim that a cause is confirmed unless the evidence supports it.
    """,
    expected_output="TODO: Define the possible-cause investigation output.",
    agent=technical_investigator,
    context=[incident_task, log_analysis_task],
    async_execution=True
)

root_cause_task = Task(
    description="""
    Review the findings from the investigation agents.

    TODO: Decide how the Root Cause Analyst should compare possible causes,
    identify the explanation best supported by the evidence, discuss
    alternatives, and state uncertainty or limitations.
    """,
    expected_output="TODO: Define the root-cause analysis output.",
    agent=root_cause_analyst,
    context=[log_analysis_task, technical_task]
)

report_task = Task(
    description="""
    Create a structured technical incident report using the completed
    investigation findings.

    TODO: Decide which sections the final report should contain. Include
    evidence, conclusions, recommended actions, and an honest statement of
    confidence or limitations.

    The report must distinguish observed evidence from assumptions.
    """,
    expected_output="TODO: Define the structure and quality requirements for the final report.",
    agent=report_generator,
    context=[incident_task, log_analysis_task, technical_task, root_cause_task]
)


# ---------------------------------------------------------
# 5. Assemble the Crew
# ---------------------------------------------------------

crew = Crew(
    agents=[
        incident_manager,
        log_analyst,
        technical_investigator,
        root_cause_analyst,
        report_generator
    ],
    tasks=[
        incident_task,
        log_analysis_task,
        technical_task,
        root_cause_task,
        report_task
    ],
    verbose=True
)


# ---------------------------------------------------------
# 6. Run the investigation
# ---------------------------------------------------------

result = crew.kickoff()


# ---------------------------------------------------------
# 7. Save the final report
# ---------------------------------------------------------

with open("output/incident_report.md", "w", encoding="utf-8") as file:
    file.write(str(result))

print("\nInvestigation complete.")
print("Report saved to: output/incident_report.md")
