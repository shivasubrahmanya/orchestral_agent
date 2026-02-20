# Multi_tasking_agent 🎻🤖

**Multi_tasking_agent** (formerly Orchestral Agent) is an advanced multi-agent system designed to autonomously generate, test, debug, and fix code. It employs a symphony of specialized AI agents working in harmony to ensure high-quality, verified software solutions.

> **Note:** Execution logs for demonstration runs have been saved to `dijkstra_execution_log.txt` and `dijkstra_solver_execution_log.txt`. See `comparison.txt` for a detailed analysis of the results.

Unlike simple "text-to-code" generators, this system follows a strict **Test-Driven Development (TDD)** workflow. It plans the architecture, writes code (that might initially be buggy), generates rigorous test suites, validates the code, and autonomously fixes any issues until the code passes all tests.

## 🌟 Features

- **Multi-Agent Architecture**: Five specialized agents (Planner, Coder, Tester, Fixer, Judge) collaborate to solve problems.
- **Automated TDD Cycle**: Enforces a Plan → Code → Test → Fail → Fix → Verify loop.
- **Self-Healing Code**: Detects failures in generated code and autonomously patches them.
- **Dual-LLM Support**:
    - **Google Gemini**: Uses `gemini-flash-latest` (Recommended). Prioritized if both keys are present.
    - **OpenAI GPT**: Uses `gpt-3.5-turbo`.
- **Robustness**: Handles API rate limits with exponential backoff and retries.
- **Mock Mode**: Includes a simulation mode to demonstrate workflows without using API credits.
- **Detailed Logging**: Provides color-coded, real-time feedback on every phase of the orchestration.

## 📂 Project Structure

```bash
orchestral_agent/
├── agents/                 # Specialized agent implementations
│   ├── planner.py          # Deconstructs goals into technical specs
│   ├── coder.py            # Generates initial (potentially buggy) code
│   ├── tester.py           # Writes pytest suites based on specs
│   ├── fixer.py            # Analyzes errors and patches code
│   ├── judge.py            # Evaluates test results (Success/Failure)
│   └── base.py             # Base agent class
├── llm/                    # LLM Interface layer
│   └── client.py           # Handles OpenAI/Gemini connections and rate limits
├── utils/                  # Utility functions
│   └── file_io.py          # File reading/writing helpers
├── generated_workspace/    # Sandbox where all code & tests are written
├── orchestrator.py         # Main entry point / Controller
├── schemas.py              # Pydantic models for structured agent communication
├── requirements.txt        # Project dependencies
└── .env                    # API keys configuration
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- An API Key for **Google Gemini** (recommended) or **OpenAI**.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shivasubrahmanya/Multi_tasking_agent.git
   cd orchestral_agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Create a `.env` file in the root directory to store your API keys.

**Option 1: Google Gemini (Recommended)**
```ini
GEMINI_API_KEY=your_gemini_api_key_here
```

**Option 2: OpenAI**
```ini
OPENAI_API_KEY=your_openai_api_key_here
```

> **Note:** If both keys are present, the system prioritizes Gemini.

## 🎮 Usage

### Interactive Mode
Simply run the orchestrator and enter your goal when prompted:
```bash
python orchestrator.py
```

### Command Line Mode
Pass your coding goal directly via the `--goal` flag:
```bash
python orchestrator.py --goal "Create a function to calculate the Nth Fibonacci number efficiently"
```

### Mock Mode (Demo)
Run a simulation without using any API credits. This uses hardcoded responses to demonstrate the agent workflow.
```bash
python orchestrator.py --mock
```

## 🧠 How It Works

The `Orchestrator` manages a sequential workflow involving specialized agents. Here is the lifecycle of a request:

1.  **Phase 1: Planning (PlannerAgent)**
    *   **Goal**: "Create a factorial function."
    *   **Action**: The Planner analyzes the request and creates a precise technical specification (`PlannerSpec`), including the filename, function signature, and step-by-step logic.

2.  **Phase 2: Coding (CoderAgent)**
    *   **Action**: The Coder implements the specification.
    *   **Note**: The system is designed to handle imperfections. The Coder might introduce a bug (intentionally or not), simulating a real-world development scenario where initial drafts are rarely perfect.

3.  **Phase 3: Writing Tests (TesterAgent)**
    *   **Action**: The Tester reviews the *specification* (not the code) and writes a comprehensive `pytest` suite to verify requirements, edge cases, and error handling.

4.  **Phase 4: Initial Testing**
    *   **Action**: The system runs the generated test against the generated code.
    *   **Expectation**: We often *expect* failure here, acting as a confirmation that the tests are running and potentially catching bugs.

5.  **Phase 5: Judgment (JudgeAgent)**
    *   **Action**: The Judge analyzes the test output. If tests fail, it marks the task for fixing. If they pass immediately, it warns that the process was too easy (or the tests might be too lenient).

6.  **Phase 6: Fixing (FixerAgent)**
    *   **Action**: The Fixer reads the **Spec**, the **Buggy Code**, and the **Test Failure Report**. It then rewrites the code to resolve the specific errors found by the tests.

7.  **Phase 7: Verification**
    *   **Action**: The system runs the tests again against the fixed code.
    *   **Final Result**: The Judge issues a final verdict: **SUCCESS** or **FAILURE**.

## 🛠️ Generated Output

All artifacts are saved in the `generated_workspace/` directory:
*   `filename.py`: The final, working code.
*   `filename_buggy.py`: The original version (for diff/backup).
*   `filename_fixed.py`: The fixed version (same as main file if fixed).
*   `test_filename.py`: The test suite.

## 🤝 Contributing

Contributions are welcome! Please feel free to inspect the `agents/` folder to add new capabilities or improve existing prompts.