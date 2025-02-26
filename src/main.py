import schedule
import time
import os
import threading
from datetime import datetime
from scheduler import schedule_commit, load_commit_history
from git_operations import is_valid_git_repo, branch_exists, get_repo_changes

def get_valid_repo_path():
  """Continuously asks for a valid Git repository path."""
  while True:
    repo_path = input("Enter the repository path: ").strip()
    if not os.path.exists(repo_path):
      print(f"Error: The path '{repo_path}' does not exist. Try again.")
      continue
    if not is_valid_git_repo(repo_path):
      print(f"Error: The path '{repo_path}' is not a valid Git repository. Try again.")
      continue
    return repo_path

def get_valid_branch(repo_path):
  """Continuously asks for a valid branch name."""
  while True:
    branch_name = input("Enter the branch name: ").strip()
    if not branch_exists(repo_path, branch_name):
      print(f"Error: Branch '{branch_name}' does not exist. Try again.")
      continue
    return branch_name

def get_valid_time():
  """Continuously asks for a valid time format (HH:MM)."""
  while True:
    commit_time = input("Enter the time to commit (HH:MM): ").strip()
    if len(commit_time) == 5 and commit_time[2] == ":":
      hh, mm = commit_time.split(":")
      if hh.isdigit() and mm.isdigit() and 0 <= int(hh) < 24 and 0 <= int(mm) < 60:
        return commit_time
    print("Error: Invalid time format. Use HH:MM (24-hour format). Try again.")

def get_files_to_commit(repo_path):
  """Ask the user to select files to commit."""
  modified, added, deleted = get_repo_changes(repo_path)

  if not (modified or added or deleted):
    print("No changes detected. Nothing to commit.")
    return []

  print("\nDetected changes:")
  index = 1
  file_map = {}

  for file_list, label in [(modified, "Modified"), (added, "Added"), (deleted, "Deleted")]:
    if file_list:
      print(f"\n{label} files:")
      for file in file_list:
        print(f"{index}. {file}")
        file_map[index] = file
        index += 1

  print("\nSelect files to commit (comma-separated numbers, or 'all' to commit everything):")
  
  while True:
    selection = input("> ").strip().lower()

    if selection == "all":
      return modified + added + deleted

    try:
      selected_indexes = [int(i) for i in selection.split(",")]
      selected_files = [file_map[i] for i in selected_indexes if i in file_map]

      if not selected_files:
        print("Error: Invalid selection. Try again.")
        continue

      return selected_files
    except ValueError:
      print("Error: Please enter numbers separated by commas, or 'all'. Try again.")

def show_commit_history():
  """Display past commit messages and scheduled times."""
  history = load_commit_history()
  if not history:
    print("\nNo previous commits found.")
    return

  print("\nPrevious Commits:")
  for i, commit in enumerate(history[-5:], start=1):  # Show last 5 commits
    print(f"{i}. [{commit['commit_time']}] {commit['commit_message']} (Branch: {commit['branch_name']})")

def countdown(commit_time):
  """Real-time countdown to commit time."""
  target_time = datetime.strptime(commit_time, "%H:%M").replace(
    year=datetime.now().year, month=datetime.now().month, day=datetime.now().day
  )
  
  while True:
    now = datetime.now()
    remaining_time = (target_time - now).total_seconds()

    if remaining_time <= 0:
      print("\nTime reached! Committing changes...\n")
      return

    minutes, seconds = divmod(int(remaining_time), 60)
    print(f"\rTime remaining: {minutes:02}:{seconds:02}", end="")
    time.sleep(1)

def main():
  print("Welcome to Git Scheduler!")
  
  show_commit_history()

  repo_path = get_valid_repo_path()
  branch_name = get_valid_branch(repo_path)
  commit_message = input("Enter the commit message: ").strip()
  commit_time = get_valid_time()

  files_to_commit = get_files_to_commit(repo_path)
  if not files_to_commit:
    print("No files selected for commit. Exiting.")
    return

  success = schedule_commit(repo_path, branch_name, commit_message, commit_time, files_to_commit)
  
  if success:
    print(f"\nCommit scheduled for {commit_time}. Sit back and relax!")

    countdown_thread = threading.Thread(target=countdown, args=(commit_time,), daemon=True)
    countdown_thread.start()

  while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
  main()
