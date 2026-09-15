# CrewAI Workshop — Part 2: AI Incident Investigation

In Part 1, you built individual agents and then combined them into a sequential CrewAI workflow.

In Part 2, you will build a small **AI incident investigation team** using CrewAI and a local Ollama model.

The application structure is already provided. Your job is to decide what each specialist should do, how the agents should collaborate, and what evidence they should use.

## What You Will Build

A five-agent investigation workflow:

```text
                    Incident Data
                         |
                         v
                [Incident Manager]
                         |
              +----------+----------+
              |                     |
              v                     v
       [Log/Data Analyst]   [Technical Investigator]
              |                     |
              +----------+----------+
                         |
                         v
                [Root Cause Analyst]
                         |
                         v
                 [Report Generator]
                         |
                         v
                  Incident Report
```

The two investigation agents run independently so that the workflow can collect different perspectives before asking another agent to determine the most likely root cause.

## Learning Goals

By the end of this activity, you should be able to:

- design specialized agent roles for a real-world problem
- write useful agent goals and backstories
- design tasks with clear instructions and expected outputs
- pass information between CrewAI tasks using `context`
- use asynchronous tasks for independent investigation work
- combine multiple findings into a final report
- think about evidence, uncertainty, and human validation

## Activity

Start by looking at the five scrambled agent cards in the workshop slides.

Decide which agent belongs in each position in the investigation workflow.

Then open `main.py` and complete the TODO sections.

### You are responsible for

1. Agent `role`
2. Agent `goal`
3. Agent `backstory`
4. Task instructions marked with TODOs
5. Expected outputs marked with TODOs
6. Deciding what information each downstream task needs through `context`

### Already provided for you

- Ollama configuration
- CSV loading
- CrewAI imports
- basic application structure
- the five-agent workflow
- asynchronous investigation task setup
- Crew creation
- kickoff code
- report file saving

This means you can focus on **agent design and workflow reasoning**, rather than spending the workshop on Python boilerplate.

## Run the Application

After completing the TODOs:

```bash
python main.py
```

The generated report will be written to:

```text
output/incident_report.md
```

## Think About the Roles

The five roles have different responsibilities:

- **Incident Manager** — What happened, what is affected, and what needs to be investigated?
- **Log/Data Analyst** — What patterns or anomalies are visible in the data?
- **Technical Investigator** — What technical causes could explain the evidence?
- **Root Cause Analyst** — Which explanation is best supported by the evidence?
- **Report Generator** — How should the investigation findings be communicated?

A useful distinction is:

```text
Technical Investigator
        |
        | What could be causing this?
        v
Possible explanations
        |
        v
Root Cause Analyst
        |
        | Which explanation is best supported?
        v
Most likely root cause
```

## Why Are Two Agents Parallel?

The Log/Data Analyst and Technical Investigator can investigate independently.

That means they do not need to wait for one another before starting their work.

In CrewAI, this can be represented with:

```python
Task(..., async_execution=True)
```

The root cause task then receives their findings through `context`.

```text
                 Incident Manager
                       |
             +---------+---------+
             |                   |
             v                   v
       Data Analysis      Technical Investigation
             |                   |
             +---------+---------+
                       |
                       v
                 Root Cause
```

## Evidence Matters

The model should not simply invent a convincing explanation.

When investigating an incident, ask:

- What does the data actually show?
- What changed before the incident?
- Which findings support a possible cause?
- Which conclusions are assumptions?
- What information is missing?
- How confident should we be?

A useful rule:

> A confident answer is not automatically a correct answer.

## Repository Structure

```text
CrewAI-Workshop-Part-2/
├── README.md
├── .gitignore
├── main.py
├── data/
│   └── incident_data.csv
├── output/
│   └── .gitkeep
└── solution/
    └── main.py
```

`main.py` contains intentional TODOs for the workshop. `solution/main.py` contains a completed version for comparison after the activity.

The setup and environment preparation are covered in Part 1, so this repository does not repeat those instructions.
