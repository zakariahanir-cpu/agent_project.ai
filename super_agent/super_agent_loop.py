import json
from .groq_interface import GroqInterface
from .file_manager import FileManager
from .git_controller import GitController
from .brain_module import BrainModule
from .tools_validator import ToolsValidator

class SuperAgentLoop:
    def __init__(self, api_key=None):
        self.grok = GroqInterface(api_key=api_key)
        self.file_manager = FileManager()
        self.git = GitController()
        self.brain = BrainModule()
        self.tools = ToolsValidator()

    def run_iteration(self, goal="Improve the agent's capabilities and fix any bugs."):
        print(f"Starting Super Agent iteration for goal: {goal}")
        
        # 1. Get Environment State
        files = self.file_manager.list_files()
        context = {}
        for f in files:
            if f.endswith('.py') or f.endswith('.yml') or f == 'requirements.txt':
                context[f] = self.file_manager.read_file(f)
        
        state = json.dumps(context, indent=2)

        # 2. Strategic Planning
        plan = self.brain.plan_task(self.grok, goal, state)
        if "error" in plan:
            print(f"Planning Error: {plan['error']}")
            return

        print(f"Reasoning: {plan.get('reasoning')}")
        self.brain.record_event("PLANNING", {"goal": goal, "reasoning": plan.get('reasoning')})

        # 3. Execution & Validation
        changes_made = False
        execution_results = []

        for step in plan.get('steps', []):
            action = step.get('action')
            path = step.get('path')
            content = step.get('content')
            
            result = {"step": step, "status": "pending"}
            
            if action == 'write':
                print(f"Action: Writing to {path}")
                write_res = self.file_manager.write_file(path, content)
                # Validate if it's a python file
                if path.endswith('.py'):
                    val_res = self.tools.validate_code(path)
                    if not val_res['success']:
                        print(f"Validation Failed for {path}: {val_res.get('stderr')}")
                        result["status"] = "failed_validation"
                        result["error"] = val_res.get('stderr')
                    else:
                        result["status"] = "success"
                        changes_made = True
                else:
                    result["status"] = "success"
                    changes_made = True
            
            elif action == 'delete':
                print(f"Action: Deleting {path}")
                self.file_manager.delete_file(path)
                result["status"] = "success"
                changes_made = True
                
            elif action == 'test':
                print("Action: Running tests")
                test_res = self.tools.run_tests()
                result["status"] = "success" if test_res['success'] else "failed_tests"
                result["output"] = test_res.get('stdout') or test_res.get('stderr')
            
            elif action == 'cmd':
                print(f"Action: Running command {content}")
                cmd_res = self.tools.run_command(content)
                result["status"] = "success" if cmd_res['success'] else "failed_cmd"
                result["output"] = cmd_res.get('stdout') or cmd_res.get('stderr')

            execution_results.append(result)

        # 4. Record Results & Commit
        self.brain.record_event("EXECUTION", execution_results)
        
        if changes_made:
            commit_msg = f"Super Agent: {goal}\n\nReasoning: {plan.get('reasoning')}"
            print("Committing and pushing changes...")
            git_res = self.git.commit_and_push(commit_msg)
            self.brain.record_event("GIT_PUSH", {"result": git_res})
            print(f"Git Result: {git_res}")
        else:
            print("No changes were made or validated.")
