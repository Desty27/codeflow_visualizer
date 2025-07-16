# Repo Visualizer and Report generation

Repo Analyzer is an automated tool that analyzes a target GitHub repository, generates a project report, architecture diagram, and sequence flow diagram using AI and static analysis, and saves these artifacts for documentation and onboarding. It can also automatically commit these outputs for traceability.

---
## Automated Diagrams & Commit Reports

This project automatically analyzes the target repository and generates the following outputs:

### Architecture Diagram

A high-level architecture diagram is generated using Mermaid.js and rendered as SVG.  
This visualizes the main components and their relationships.

![Architecture Diagram](https://github.com/Desty27/codeflow_visualizer/blob/main/assets/Screenshot%202025-07-16%20162243.png)

---

### Sequence Flow Diagram

A sequence flow diagram is created to illustrate the dynamic interactions and flow between components or functions during execution.

![Sequence Flow Diagram](https://github.com/Desty27/codeflow_visualizer/blob/main/assets/Screenshot%202025-07-16%20162258.png)

---

### Automated Commit Reports

After generating the diagrams and project report, the tool automatically commits these artifacts to your repository. This ensures that documentation and visualizations are always up to date with the latest codebase.

'''
    # Commit Report: 14da70f
    
    ## Commit Details
    - **SHA**: `14da70f`
    - **Author**: `megadose`
    - **Date**: Not explicitly available
    - **Message**: Merge pull request #194 from secureman/master
    
    This commit merges changes from the `secureman` branch into the main project repository.
    
    ## Changes
    - **Updated Files**:
      - `core.py`: Fixes an issue with error message printing.
      - `instruments.py`: Reimplements the `tqdm` progress bar using `Trio`.
      - `localuseragent.py`: Adds an iOS-specific user-agent.
    
    ## Statistics
    - **Total Files Changed**: 3
    
    ## GPT-4o Project Flow Analysis
    
    This project, **holehe**, appears to be an investigative security tool aimed at enumerating accounts tied to a single email across multiple services. Here’s how its structure supports functionality:
    
    ### 1. The Main Function That Starts the Project
    
    - **Execution Start**: The project begins by initializing the necessary modules within `__init__.py`. This file organizes the startup configurations and dependencies.
    - **Core Functionality (`core.py`)**: This script defines essential functions, including logic for account enumeration across multiple online services.
    
    ### 2. The Order in Which Key Functions Are Called
    
    1. **User Input**: The email to be checked is provided.
    2. **Enumeration Logic (`core.py`)**: The script scans various online platforms to check the existence of the provided email.
    3. **Progress Tracking (`instruments.py`)**: Displays an improved progress bar for better UI/UX feedback.
    4. **Agent Spoofing (`localuseragent.py`)**: Implements an iOS-specific user agent to enhance API interactions.
    
    ### 3. How Data Flows Between Functions and Files
    
    - **Data Input**: The tool accepts an email as input.
    - **Processing**:
      - Calls verification functions in `core.py`.
      - Uses helper scripts (`instruments.py`) to track and format results.
    - **Output**:
      - Returns findings on whether the email is linked to accounts on different services.
    
    ### 4. What Each File is Responsible For
    
    - **`__init__.py`**: Entry point for initializing necessary modules.
    - **`core.py`**: The primary logic for checking accounts tied to an email.
    - **`instruments.py`**: Reimplements `tqdm` progress visualization using `Trio`.
    - **`localuseragent.py`**: Adds an iOS-specific user-agent.


'''



---

#### How It Works

- The tool clones the target repository and analyzes its structure.
- It uses AI and static analysis to extract architectural and flow information.
- Mermaid.js definitions are generated for both architecture and sequence diagrams.
- The [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) (`mmdc`) renders these diagrams as SVG images.
- All outputs (report, diagrams) are saved and automatically committed to the repository for traceability.

---

For more details, see the output files in the `assets/` directory after running the tool.
## Directory Structure

```
repo_analyzer/
│
├── assets/                       # Output diagrams and images (SVG, PNG)
│   ├── architecture_diagram.svg
│   ├── sequence_flow_diagram.svg
│   └── commit_report_example.png
│
├── outputs/                      # Generated reports and diagrams
│   ├── project_report.md
│   ├── high_level_diagram.svg
│   └── code_level_diagram.svg
│
├── src/                          # Source code modules
│   ├── __init__.py
│   ├── utils.py                  # Utilities: repo cloning, file ops, etc.
│   ├── analyzer.py               # AI/static analysis, artifact generation
│   └── mermaid_renderer.py       # Mermaid.js diagram rendering
│
├── .env                          # Environment variables (API keys, etc.)
├── requirements.txt              # Python dependencies
├── main.py                       # Entry point: orchestrates analysis and output
├── README.md                     # Project documentation
└── LICENSE
```

---

## Tech Stack

- **Python 3.8+**  
  Main language for orchestration, analysis, and artifact management.
- **OpenAI API**  
  For AI-powered code summarization and documentation.
- **GitPython**  
  For repository cloning and git operations.
- **Mermaid.js CLI (`mmdc`)**  
  For rendering architecture and sequence diagrams from Mermaid definitions.
- **dotenv**  
  For managing environment variables.
- **Other dependencies:**  
  `requests`, `os`, `sys`, etc.

---

## Workflow

1. **Environment Check:**  
   Ensures all required tools (Python packages, Mermaid CLI) are installed.
2. **Repository Cloning:**  
   Clones the target repository using GitPython.
3. **Code Structure Extraction:**  
   Analyzes the codebase to extract structure and relationships.
4. **Artifact Generation:**  
   Uses AI (OpenAI API) and static analysis to generate:
   - Project report (Markdown)
   - Architecture diagram (Mermaid → SVG)
   - Sequence flow diagram (Mermaid → SVG)
5. **Saving Outputs:**  
   All generated artifacts are saved to the `assets/` or `outputs/` directory.
6. **Automated Commit Reports:**  
   Optionally, commits the new/updated artifacts to the repository for traceability.

---




## Example Output

After running the tool, you’ll see output like:
```
✅ Analysis complete!

📄 Output files:
- Project report: outputs/project_report.md
- High-level diagram: outputs/high_level_diagram.svg
- Code-level diagram: outputs/code_level_diagram.svg
```

---

## Usage

```bash
python main.py
```

---

##
