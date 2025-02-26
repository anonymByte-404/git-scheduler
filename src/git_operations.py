import schedule
import json
import os
from datetime import datetime
from git_operations import commit_and_push

if not os.path.exists("data"):
    os.makedirs("data")

HISTORY_FILE = "data/commit_history.json"

def save_commit_history(repo_path, branch_name, commit_message, commit_time):
  """Save commit details to a JSON file for future reference."""
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
  """Load commit history from a JSON file."""
  if not os.path.exists(HISTORY_FILE):
    return []
  with open(HISTORY_FILE, "r") as f:
    return json.load(f)

def schedule_commit(repo_path, branch_name, commit_message, commit_time, files_to_commit):
  """Schedules a commit and saves it to history."""
  if not files_to_commit:
    print("Error: No files selected for commit. Aborting.")
    return False

  schedule.every().day.at(commit_time).do(
    commit_and_push, repo_path=repo_path, branch_name=branch_name, commit_message=commit_message, files_to_commit=files_to_commit
  )
  
  save_commit_history(repo_path, branch_name, commit_message, commit_time)
  return True
