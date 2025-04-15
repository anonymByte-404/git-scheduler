import schedule
from typing import List
from git_operations import commit_and_push, save_commit_history

def schedule_commit(
  repo_path: str,
  branch_name: str,
  commit_message: str,
  commit_time: str,
  files_to_commit: List[str]
) -> bool:
  """Schedule a daily commit task at a specific time."""
  if not files_to_commit:
    print("Error: No files selected for commit.")
    return False

  schedule.every().day.at(commit_time).do(
    commit_and_push,
    repo_path=repo_path,
    branch_name=branch_name,
    commit_message=commit_message,
    files_to_commit=files_to_commit
  )

  save_commit_history(repo_path, branch_name, commit_message, commit_time)
  return True
