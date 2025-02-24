import subprocess

def commit_and_push(repo_path, branch_name, commit_message):
  try:
    result = subprocess.run(["git", "add", "."], cwd=repo_path, check=True, capture_output=True, text=True)
    print(result.stdout, result.stderr)

    result = subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True, capture_output=True, text=True)
    print(result.stdout, result.stderr)

    result = subprocess.run(["git", "push", "origin", branch_name], cwd=repo_path, check=True, capture_output=True, text=True)
    print(result.stdout, result.stderr)

    print(f"Successfully committed and pushed to {branch_name}.")
  except subprocess.CalledProcessError as e:
    print(f"Error: {e.stderr}")
