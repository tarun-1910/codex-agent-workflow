# Codex Agent Workflow

An AI-powered multi-agent software development workflow built with Python and Codex. The system uses specialized AI agents to plan, design, develop, and review software applications through an automated workflow.

## Overview

Codex Agent Workflow automates multiple stages of the Software Development Life Cycle (SDLC) using five specialized agents.

Instead of manually performing every development stage, users provide a project idea, and the agents collaborate to generate project requirements, architecture, frontend code, backend code, and testing reports.

## Architecture

```text
                 User Project Idea
                        |
                        v
                Workflow Orchestrator
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
     Project         Designer      Developer
     Manager          Agent         Agents
          |             |          /       \
          v             v         v         v
     Requirements   Design     Frontend   Backend
       Documents   Specification Developer Developer
                                    |         |
                                    v         v
                                 HTML/CSS   FastAPI
                                 JavaScript SQLite
                                    \         /
                                     \       /
                                      v     v
                                    Tester
                                      |
                                      v
                                  Test Report
```

## Specialized Agents

### 1. Project Manager Agent

Responsible for analyzing the project idea and generating project planning documents.

**Responsibilities:**
- Analyze project requirements.
- Identify functional requirements.
- Identify non-functional requirements.
- Break down development tasks.
- Define acceptance criteria.

**Generated files:**
- `requirements.md`
- `tasks.md`
- `acceptance_criteria.md`

### 2. Designer Agent

Responsible for converting project requirements into a technical and UI/UX design specification.

**Responsibilities:**
- Define application architecture.
- Design database schema.
- Specify API endpoints.
- Define frontend components and pages.
- Document application workflows.
- Identify design considerations and risks.

**Generated file:**
- `design_spec.md`

### 3. Frontend Developer Agent

Responsible for generating the application's frontend based on the design specification.

**Responsibilities:**
- Generate HTML structure.
- Implement CSS styling.
- Develop JavaScript functionality.
- Implement user interactions.
- Create responsive interfaces.

**Generated files:**
- `index.html`
- `style.css`
- `script.js`

**Technologies:** HTML5, CSS3, JavaScript.

### 4. Backend Developer Agent

Responsible for generating backend services and database functionality.

**Responsibilities:**
- Develop REST APIs.
- Implement CRUD operations.
- Create database connections.
- Implement input validation.
- Handle API errors.
- Configure CORS.

**Generated files:**
- `main.py`
- `database.py`
- `requirements.txt`

**Technologies:** Python, FastAPI, SQLite, Pydantic.

### 5. Tester Agent

Responsible for reviewing the generated application and identifying potential issues.

**Responsibilities:**
- Review frontend implementation.
- Review backend implementation.
- Analyze database operations.
- Identify integration problems.
- Check requirement coverage.
- Categorize issues by severity.
- Suggest possible fixes.

**Generated file:**
- `test_report.json`

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Agent implementation and orchestration |
| Codex | AI-powered coding and reasoning engine |
| HTML | Frontend structure |
| CSS | Frontend styling |
| JavaScript | Frontend functionality |
| FastAPI | Backend API development |
| SQLite | Database |
| Pydantic | Data validation |
| JSON | Agent response format |
| Markdown | Requirements and design documentation |
| Git | Version control |

## Project Structure

```text
codex-agent-workflow/
│
├── agents/
│   ├── project_manager.py
│   ├── designer.py
│   ├── frontend_developer.py
│   ├── backend_developer.py
│   └── tester.py
│
├── orchestrator/
│   ├── workflow.py
│   ├── handoffs.py
│   └── task_manager.py
│
├── core/
│   ├── codex_client.py
│   ├── file_validator.py
│   └── trace_logger.py
│
├── workspace/
│   └── generated_project/
│
├── traces/
│
├── main.py
├── config.py
├── README.md
└── requirements.txt
```

*Note: Some planned modules, such as handoffs, task management, file validation, and trace logging, are reserved for future implementation.*

## Installation and Setup

### Prerequisites

- Python 3.10 or higher.
- Codex CLI installed.
- VS Code or another Python IDE.
- Git (optional).

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/codex-agent-workflow.git

cd codex-agent-workflow
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

Install the Codex SDK package and the dependencies required by your project environment.

```bash
pip install -r requirements.txt
```

### 4. Authenticate with Codex

Install Codex CLI if it is not already installed, then authenticate using your ChatGPT account:

```bash
codex login
```

Follow the authentication instructions displayed in your terminal.

This project is designed to use your Codex account authentication rather than requiring a separate OpenAI API key.

### 5. Run the workflow

```bash
python main.py
```

## Example Input

```python
project_idea = """
Build a Task Management application called TaskFlow.

Features:
- Create tasks.
- View all tasks.
- Update tasks.
- Delete tasks.
- Change task status.
- Track task creation dates.

Technology:
- Frontend: HTML, CSS, JavaScript.
- Backend: Python FastAPI.
- Database: SQLite.
- Testing: Pytest.
"""
```

## Example Output

After successful execution, the workflow generates:

```text
generated_project/
│
├── requirements.md
├── tasks.md
├── acceptance_criteria.md
├── design_spec.md
├── test_report.json
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── backend/
    ├── main.py
    ├── database.py
    └── requirements.txt
```

## Current Workflow

The current implementation executes the five agents sequentially:

1. Project Manager generates requirements.
2. Designer generates the design specification.
3. Frontend Developer generates frontend code.
4. Backend Developer generates backend code.
5. Tester reviews the generated application and creates a test report.

Run the complete workflow using:

```bash
python main.py
```

## Current Limitations

The current version is an initial implementation.

- Frontend and backend integration is not yet fully implemented.
- Testing currently relies on AI-based code review rather than comprehensive automated test execution.
- Failed issues are reported but are not automatically routed back to developers.
- Agents currently execute sequentially.
- Automatic retries and approval gates are not yet implemented.

## Future Enhancements

- **Automated Agent Handoffs:** Transfer outputs and tasks between specialized agents.
- **Parallel Agent Execution:** Allow frontend and backend developers to work simultaneously.
- **Automatic Bug Fixing:** Route Tester findings to the responsible developer.
- **Retry Mechanism:** Retry failed tasks with configurable limits.
- **Context Isolation:** Provide each agent with only the necessary project context.
- **Human-in-the-Loop Approval:** Require approval for sensitive operations.
- **Git Checkpoints:** Create recoverable versions of generated code.
- **Automated Testing:** Execute Pytest and API integration tests.
- **Observability and Tracing:** Track agent execution, decisions, failures, and performance.

## Project Goal

The goal of this project is to explore how specialized AI agents can collaborate to automate software development workflows.

It demonstrates the application of AI agents, prompt engineering, task orchestration, code generation, and automated software review within a structured SDLC process.

---

**Project:** Codex Agent Workflow  
**Language:** Python  
**Coding Engine:** Codex  
**Architecture:** Multi-Agent System  
**Status:** Initial Implementation / Active Development
