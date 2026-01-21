import os
import sys
import subprocess
import argparse
import logging
from colorama import init, Fore, Style

from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from agents.tester import TesterAgent
from agents.fixer import FixerAgent
from agents.judge import JudgeAgent
from utils.file_io import write_file, read_file

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("Orchestrator")

WORK_DIR = "generated_workspace"

class Orchestrator:
    def __init__(self, use_mock: bool = False):
        self.planner = PlannerAgent(use_mock=use_mock)
        self.coder = CoderAgent(use_mock=use_mock)
        self.tester = TesterAgent(use_mock=use_mock)
        self.fixer = FixerAgent(use_mock=use_mock)
        self.judge = JudgeAgent(use_mock=use_mock)
        
    def run_command(self, cmd):
        """Runs a shell command and returns stdout + stderr."""
        logger.info(f"{Fore.YELLOW}Executing: {' '.join(cmd)}")
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=WORK_DIR
        )
        return result.stdout + result.stderr

    def start(self, goal: str):
        logger.info(f"{Fore.CYAN}{Style.BRIGHT}=== Starting Orchestral Agent System ===")
        logger.info(f"Goal: {goal}")
        
        # Ensure work dir exists
        os.makedirs(WORK_DIR, exist_ok=True)

        # 1. PLANNER
        logger.info(f"\n{Fore.BLUE}--- Phase 1: Planning ---")
        spec = self.planner.run(goal)
        logger.info(f"Plan created: {spec.filename} -> {spec.function_name}")
        logger.info(f"Steps: {spec.steps}")

        # 2. CODER (Generates Buggy Code)
        logger.info(f"\n{Fore.BLUE}--- Phase 2: Coding (Intentional Bug) ---")
        coder_out = self.coder.run(spec)
        code_path = os.path.join(WORK_DIR, spec.filename)
        buggy_path = os.path.join(WORK_DIR, spec.filename.replace(".py", "_buggy.py"))
        
        # Save both for history
        write_file(code_path, coder_out.file_content)
        write_file(buggy_path, coder_out.file_content)
        logger.info(f"Code written to {code_path} (Backup: {buggy_path})")

        # 3. TESTER
        logger.info(f"\n{Fore.BLUE}--- Phase 3: Writing Tests ---")
        tester_out = self.tester.run(spec)
        test_filename = f"test_{spec.filename}"
        test_path = os.path.join(WORK_DIR, test_filename)
        write_file(test_path, tester_out.test_content)
        logger.info(f"Tests written to {test_path}")

        # 4. INITIAL TEST RUN (Expect Fail)
        logger.info(f"\n{Fore.BLUE}--- Phase 4: Initial Testing ---")
        test_output = self.run_command(["pytest", test_filename])
        logger.info("Test Output (Truncated):")
        print(test_output[:500] + "..." if len(test_output) > 500 else test_output)

        # 5. JUDGE (Check failure)
        judge_verdict = self.judge.run(test_output)
        if judge_verdict.success:
            logger.warning(f"{Fore.RED}WARNING: Tests passed unexpectedly! The Coder failed to insert a bug.")
        else:
            logger.info(f"{Fore.GREEN}Confirmation: Tests failed as expected. Proceeding to fix.")

        # 6. FIXER
        logger.info(f"\n{Fore.BLUE}--- Phase 5: Fixing ---")
        # Read the current broken code
        current_code = read_file(code_path)
        fixer_out = self.fixer.run(spec, current_code, test_output)
        
        # Save fixed version
        write_file(code_path, fixer_out.file_content) # Overwrite main file for testing
        fixed_path = os.path.join(WORK_DIR, spec.filename.replace(".py", "_fixed.py"))
        write_file(fixed_path, fixer_out.file_content) # Save snapshot
        
        logger.info(f"Fixed code written to {code_path} (Snapshot: {fixed_path})")

        # 7. VERIFICATION TEST RUN
        logger.info(f"\n{Fore.BLUE}--- Phase 6: Verification Testing ---")
        final_test_output = self.run_command(["pytest", test_filename])
        logger.info("Final Test Output (Truncated):")
        print(final_test_output[:500] + "..." if len(final_test_output) > 500 else final_test_output)

        # 8. FINAL JUDGEMENT
        logger.info(f"\n{Fore.BLUE}--- Phase 7: Final Judgment ---")
        final_verdict = self.judge.run(final_test_output)
        
        if final_verdict.success:
            logger.info(f"{Fore.GREEN}{Style.BRIGHT}SUCCESS: {final_verdict.reason}")
            logger.info(f"\n{Fore.CYAN}=== Generated Files ===")
            logger.info(f"Buggy Code: {os.path.abspath(buggy_path)}")
            logger.info(f"Fixed Code: {os.path.abspath(fixed_path)}")
            logger.info(f"Test Suite: {os.path.abspath(test_path)}")
        else:
            logger.error(f"{Fore.RED}{Style.BRIGHT}FAILURE: {final_verdict.reason}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orchestral Agent Prototype")
    parser.add_argument("--goal", type=str, help="The coding task to perform.")
    parser.add_argument("--mock", action="store_true", help="Use mock LLM responses for demonstration without API key.")
    args = parser.parse_args()

    orchestrator = Orchestrator(use_mock=args.mock)
    
    # improved input handling
    goal = args.goal
    if not goal:
        print(f"\n{Fore.GREEN}Please enter your coding goal:")
        goal = input(f"{Fore.RESET}> ")
    
    orchestrator.start(goal)
