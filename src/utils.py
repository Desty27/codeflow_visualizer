import os
import re
from git import Repo

def clone_repository(repo_url):
    """Clone GitHub repository"""
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    if os.path.exists(repo_name):
        print(f"Repository {repo_name} already exists. Using cached version.")
        return repo_name
        
    print(f"Cloning repository: {repo_url}")
    Repo.clone_from(repo_url, repo_name)
    return repo_name

def get_code_structure(repo_path):
    """Extract code structure with file contents"""
    code_structure = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    try:
                        code_structure[path] = f.read()
                    except UnicodeDecodeError:
                        # Skip binary files
                        continue
    return code_structure