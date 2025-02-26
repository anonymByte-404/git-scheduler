import schedule
from git_operations import commit_and_push

def schedule_commit(repo_path, branch_name, commit_message, commit_time, files_to_commit):
  """Schedules a commit only if selected files exist."""
  if not files_to_commit:
    print("Error: No files selected for commit. Aborting.")
    return False

  schedule.every().day.at(commit_time).do(
    commit_and_push, repo_path=repo_path, branch_name=branch_name, commit_message=commit_message, files_to_commit=files_to_commit
  )
  
  return True
