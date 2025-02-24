import schedule
from git_operations import commit_and_push

def schedule_commit(repo_path, branch_name, commit_message, commit_time):
  schedule.every().day.at(commit_time).do(
    commit_and_push, repo_path=repo_path, branch_name=branch_name, commit_message=commit_message
  )
