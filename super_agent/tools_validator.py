import subprocess
import os

class ToolsValidator:
    def __init__(self, base_dir="."):
        self.base_dir = os.path.abspath(base_dir)

    def run_command(self, command):
        try:
            # Command can be a list or a string
            shell = isinstance(command, str)
            result = subprocess.run(
                command,
                cwd=self.base_dir,
                capture_output=True,
                text=True,
                shell=shell,
                timeout=60
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def run_tests(self):
        print("Running tests...")
        # Try running pytest if available, otherwise use unittest
        result = self.run_command(["python3", "-m", "unittest", "discover", "tests"])
        return result

    def validate_code(self, file_path):
        # Basic syntax check
        result = self.run_command(["python3", "-m", "py_compile", file_path])
        return result
