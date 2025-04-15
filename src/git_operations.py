import os
import json
import subprocess
from datetime import datetime
from typing import List, Tuple, TypedDict, Any

class Constant:
  """A class to define an immutable constant value."""
  def __init__(self, value: Any) -> None:
    self._value: Any = value

  @property
  def value(self) -> Any:
    return self._value

  @value.setter
  def value(self, value: Any) -> None:
    raise AttributeError("Can't modify a constant.")

BASE_DIR: Constant = Constant(os.path.dirname(__file__))
DATA_DIR: Constant = Constant(os.path.join(BASE_DIR.value, "data"))
HISTORY_FILE: Constant = Constant(os.path.join(DATA_DIR.value, "commit_history.json"))

class CommitEntry(TypedDict):
  """Typed dictionary structure for commit history entries."""
  repo_path: str
  branch_name: str
  commit_message: str
  commit_time: str
  scheduled_at: str

def is_valid_git_repo(path: str) -> bool:
  """Check if a path is a valid Git repository."""
  return os.path.isdir(os.path.join(path, ".git"))

def branch_exists(repo_path: str, branch: str) -> bool:
  """Check if a Git branch exists in the repository."""
  try:
    result = subprocess.run(
      ["git", "branch", "--list", branch],
      cwd=repo_path, stdout=subprocess.PIPE, text=True
    )
    return branch in result.stdout
  except Exception:
    return False

def get_repo_changes(repo_path: str) -> Tuple[List[str], List[str], List[str]]:
  """Get lists of modified, added, and deleted files in the repo."""
  try:
    result = subprocess.run(
      ["git", "status", "--porcelain"],
      cwd=repo_path, stdout=subprocess.PIPE, text=True
    )
    lines = result.stdout.strip().split("\n")

    modified: List[str] = []
    added: List[str] = []
    deleted: List[str] = []

    for line in lines:
      if not line:
        continue
      status = line[:2]
      file = line[3:]
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

def commit_and_push(repo_path: str, branch_name: str, commit_message: str, files_to_commit: List[str]) -> None:
  """Commit and push selected files to a Git branch."""
  try:
    subprocess.run(["git", "checkout", branch_name], cwd=repo_path, check=True)
    subprocess.run(["git", "add"] + files_to_commit, cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
    subprocess.run(["git", "push", "origin", branch_name], cwd=repo_path, check=True)
    print(f"✔ Pushed to '{branch_name}' successfully.")
  except subprocess.CalledProcessError as e:
    print(f"✖ Git command failed: {e}")

def save_commit_history(repo_path: str, branch_name: str, commit_message: str, commit_time: str) -> None:
  """Save commit information to the commit history file."""
  os.makedirs(DATA_DIR.value, exist_ok=True)
  history: List[CommitEntry] = load_commit_history()
  history.append({
    "repo_path": repo_path,
    "branch_name": branch_name,
    "commit_message": commit_message,
    "commit_time": commit_time,
    "scheduled_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  })
  with open(HISTORY_FILE.value, "w") as f:
    json.dump(history, f, indent=2)

def load_commit_history() -> List[CommitEntry]:
  """Load the commit history from the history file."""
  if not os.path.exists(HISTORY_FILE.value):
    return []
  with open(HISTORY_FILE.value, "r") as f:
    return json.load(f)
