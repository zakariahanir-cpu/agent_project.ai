import os
import shutil

class FileManager:
    def __init__(self, base_dir="."):
        self.base_dir = os.path.abspath(base_dir)

    def read_file(self, file_path):
        full_path = os.path.join(self.base_dir, file_path)
        if not os.path.exists(full_path):
            return f"Error: File {file_path} does not exist."
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()

    def write_file(self, file_path, content):
        full_path = os.path.join(self.base_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Success: File {file_path} written."

    def delete_file(self, file_path):
        full_path = os.path.join(self.base_dir, file_path)
        if os.path.exists(full_path):
            if os.path.isfile(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
            return f"Success: {file_path} deleted."
        return f"Error: {file_path} does not exist."

    def list_files(self, recursive=True):
        files_list = []
        for root, dirs, files in os.walk(self.base_dir):
            if '.git' in dirs or '__pycache__' in dirs:
                if '.git' in dirs: dirs.remove('.git')
                if '__pycache__' in dirs: dirs.remove('__pycache__')
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), self.base_dir)
                files_list.append(rel_path)
            if not recursive:
                break
        return files_list
