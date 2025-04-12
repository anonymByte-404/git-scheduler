import os
import time
import threading
from datetime import datetime
import schedule

from scheduler import schedule_commit, load_commit_history
from git_operations import (
  is_valid_git_repo,
  branch_exists,
  get_repo_changes
)

def get_valid_repo_path():
  """Prompt and validate Git repository path."""
  while True:
    repo_path = input("Enter the repository path: ").strip()
    if not os.path.exists(repo_path):
      print(f"Error: '{repo_path}' does not exist. Try again.")
    elif not is_valid_git_repo(repo_path):
      print(f"Error: '{repo_path}' is not a valid Git repository. Try again.")
    else:
      return repo_path

def get_valid_branch(repo_path):
  """Prompt and validate Git branch name."""
  while True:
    branch = input("Enter the branch name: ").strip()
    if branch_exists(repo_path, branch):
      return branch
    print(f"Error: Branch '{branch}' does not exist. Try again.")

def get_valid_time():
  """Prompt and validate time in HH:MM format."""
  while True:
    time_str = input("Enter commit time (HH:MM 24-hour): ").strip()
    try:
      datetime.strptime(time_str, "%H:%M")
      return time_str
    except ValueError:
      print("Error: Invalid format. Use HH:MM.")

def get_files_to_commit(repo_path):
  """Prompt user to select changed files for commit."""
  modified, added, deleted = get_repo_changes(repo_path)
  if not (modified or added or deleted):
    print("No changes detected.")
    return []

  index = 1
  file_map = {}

  print("\nDetected changes:")
  for category, files in [("Modified", modified), ("Added", added), ("Deleted", deleted)]:
    if files:
      print(f"\n{category} files:")
      for file in files:
        print(f"{index}. {file}")
        file_map[index] = file
        index += 1

  while True:
    selection = input("\nSelect files (e.g., 1,2 or 'all'): ").strip().lower()
    if selection == "all":
      return modified + added + deleted

    try:
      indices = list(map(int, selection.split(",")))
      selected = [file_map[i] for i in indices if i in file_map]
      if selected:
        return selected
    except ValueError:
      pass
    print("Error: Invalid selection. Try again.")

def show_commit_history():
  """Show last 5 commits from history."""
  history = load_commit_history()
  if not history:
    print("\nNo previous commits found.")
    return

  print("\nPrevious Commits:")
  for i, commit in enumerate(history[-5:], start=1):
    print(f"{i}. [{commit['commit_time']}] {commit['commit_message']} (Branch: {commit['branch_name']})")

def countdown_timer(commit_time):
  """Show countdown until commit time."""
  target = datetime.strptime(commit_time, "%H:%M").replace(
    year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
  )

  while True:
    now = datetime.now()
    seconds_left = (target - now).total_seconds()
    if seconds_left <= 0:
      print("\nCommit time reached!")
      return
    minutes, seconds = divmod(int(seconds_left), 60)
    print(f"\rTime remaining: {minutes:02}:{seconds:02}", end="")
    time.sleep(1)

def main():
  """Main function to run Git scheduler."""
  print("== Git Commit Scheduler ==")
  show_commit_history()

  repo_path = get_valid_repo_path()
  branch = get_valid_branch(repo_path)
  message = input("Enter commit message: ").strip()
  commit_time = get_valid_time()
  files = get_files_to_commit(repo_path)

  if not files:
    print("No files selected. Exiting.")
    return

  if schedule_commit(repo_path, branch, message, commit_time, files):
    print(f"\n✔ Commit scheduled for {commit_time}.")
    threading.Thread(target=countdown_timer, args=(commit_time,), daemon=True).start()

  while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
  main()
