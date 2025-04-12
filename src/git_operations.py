import os
import json
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
HISTORY_FILE = os.path.join(DATA_DIR, "commit_history.json")

def is_valid_git_repo(path):
  """Check if path is a Git repository."""
  return os.path.isdir(os.path.join(path, ".git"))

def branch_exists(repo_path, branch):
  """Check if branch exists in the repo."""
  try:
    result = subprocess.run(["git", "branch", "--list", branch],
                            cwd=repo_path, stdout=subprocess.PIPE, text=True)
    return branch in result.stdout
  except Exception:
    return False

def get_repo_changes(repo_path):
  """Get modified, added, and deleted files."""
  try:
    result = subprocess.run(["git", "status", "--porcelain"],
                            cwd=repo_path, stdout=subprocess.PIPE, text=True)
    lines = result.stdout.strip().split("\n")

    modified, added, deleted = [], [], []
    for line in lines:
      if not line:
        continue
      status, file = line[:2], line[3:]
      if "M" in status:
        modified.append(file)
      elif "A" in status:
        added.append(file)
      elif "D" in status:
        deleted.append(file)
    return modified, added, deleted
  except Exception as e:
    print(f"Error reading repo changes: {e}")
    return [], [], []

def commit_and_push(repo_path, branch_name, commit_message, files_to_commit):
  """Add, commit, and push selected files."""
  try:
    subprocess.run(["git", "checkout", branch_name], cwd=repo_path, check=True)
    subprocess.run(["git", "add"] + files_to_commit, cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
    subprocess.run(["git", "push", "origin", branch_name], cwd=repo_path, check=True)
    print(f"✔ Pushed to '{branch_name}' successfully.")
  except subprocess.CalledProcessError as e:
    print(f"✖ Git command failed: {e}")

def save_commit_history(repo_path, branch_name, commit_message, commit_time):
  """Save commit details to history file."""
  os.makedirs(DATA_DIR, exist_ok=True)
  history = load_commit_history()
  history.append({
    "repo_path": repo_path,
    "branch_name": branch_name,
    "commit_message": commit_message,
    "commit_time": commit_time,
    "scheduled_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  })
  with open(HISTORY_FILE, "w") as f:
    json.dump(history, f, indent=2)

def load_commit_history():
  """Load commit history from file."""
  if not os.path.exists(HISTORY_FILE):
    return []
  with open(HISTORY_FILE, "r") as f:
    return json.load(f)
