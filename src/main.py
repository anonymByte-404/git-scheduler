import schedule
import time
from scheduler import schedule_commit

def main():
  print("Welcome to Git Scheduler!")
  repo_path = input("Enter the repository path: ").strip()
  branch_name = input("Enter the branch name: ").strip()
  commit_message = input("Enter the commit message: ").strip()
  commit_time = input("Enter the time to commit (HH:MM): ").strip()

  schedule_commit(repo_path, branch_name, commit_message, commit_time)
  print(f"Commit scheduled for {commit_time}. Sit back and relax!")

  while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
  main()
