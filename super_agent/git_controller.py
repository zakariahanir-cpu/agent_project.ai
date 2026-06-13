import subprocess
import os

class GitController:
    def __init__(self, repo_path="."):
        self.repo_path = os.path.abspath(repo_path)

    def run_command(self, command):
        try:
            result = subprocess.run(
                command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"

    def commit_and_push(self, message, branch="main"):
        self.run_command(["git", "config", "user.name", "github-actions[bot]"])
        self.run_command(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
        self.run_command(["git", "add", "."])
        # Check if there are changes
        status = self.run_command(["git", "status", "--porcelain"])
        if not status.strip():
            return "Nothing to commit."
            
        commit_result = self.run_command(["git", "commit", "-m", message])
        push_result = self.run_command(["git", "push", "origin", branch])
        return f"Commit: {commit_result}\nPush: {push_result}"
