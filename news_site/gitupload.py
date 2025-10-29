import git
import os

def push_to_github(repo_dir, commit_message, branch_name='main'):
    print("Pushing repo to github")
    # Retrieve the GitHub token from the environment variable
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable not set")
    
    # Get the remote URL from the repository
    repo = git.Repo(repo_dir)
    origin = repo.remote(name='origin')
    remote_url = origin.url
    
    # Modify the remote URL to include the token for HTTPS authentication
    if remote_url.startswith("https://"):
        remote_url = remote_url.replace("https://", f"https://{github_token}@")
    else:
        raise ValueError("Remote URL must start with https://")

    # Set the new remote URL with the token for authentication
    origin.set_url(remote_url)
    
    # Stage all changes
    repo.git.add(A=True)
    
    # Commit the changes
    repo.index.commit(commit_message)
    
    # Push the changes to the remote repository
    origin.push(refspec=f"{branch_name}:{branch_name}")
    
    # Restore the original remote URL to avoid exposing the token
    origin.set_url(remote_url.replace(f"https://{github_token}@", "https://"))

if __name__ == "__main__":
    # Define your repository directory
    repo_dir = '/path/to/your/repo'  # Update this with the path to your local repository
    
    # Define your commit message
    commit_message = 'Your commit message'
    
    # Define your branch name (default is 'main')
    branch_name = 'main'
    
    # Push to GitHub
    push_to_github(repo_dir, commit_message, branch_name)

