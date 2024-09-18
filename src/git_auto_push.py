import os
import subprocess
import datetime
from git import Repo, GitCommandError
from log import get_logger
logger = get_logger(__name__)

def configure_git_user(git_username, git_email):
    """Configure global Git user name and email."""
    try:
        if git_username:
            subprocess.run(
                ["git", "config", "--global", "user.name", git_username],
                check=True
            )
            logger.info(f"Configured git username: {git_username}")

        if git_email:
            subprocess.run(
                ["git", "config", "--global", "user.email", git_email],
                check=True
            )
            logger.info(f"Configured git email: {git_email}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to configure git user: {e}")
        raise

def add_safe_directory(dirfile):
    """Add directory to Git safe.directory configuration."""
    try:
        subprocess.run(
            ["git", "config", "--global", "--add", "safe.directory", dirfile],
            check=True
        )
        logger.info(f"Added {dirfile} to git safe.directory")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to add safe directory: {dirfile}, error: {e}")
        raise

def git_auto_push(git_repo_paths=None, git_message=None, git_username=None, git_email=None):
    """Automate the process of pushing to multiple Git repositories."""
    # Configure Git user information
    configure_git_user(git_username, git_email)

    repo_paths = git_repo_paths.split("\n")
    logger.info(f"Git repository paths: {git_repo_paths}")
    
    # Process multiple repository paths and branches
    for repo_path in repo_paths:
        try:
            repo_path = repo_path.strip()
            if not repo_path:
                continue
            logger.info(f"Processing repository info: {repo_path}")
            # Split path and branch
            path, branch =  repo_path.split(" ")
            path = os.path.abspath(path)
            if not os.path.exists(path):
                logger.warning(f"Path '{path}' does not exist, skipping...")
                continue
            logger.info(f"Processing repository '{path}' with branch '{branch}'")

            dirfile = os.path.abspath(path)
            
            # Add directory to safe.directory configuration
            add_safe_directory(dirfile)

            # Initialize repository object
            repo = Repo(dirfile)

            # Ensure on the correct branch
            repo.git.checkout(branch)
            logger.info(f"Checked out to branch '{branch}' in repository '{dirfile}'")

            # Add all changes
            repo.git.add("--all")
            logger.info(f"Added all changes in repository '{dirfile}'")

            # Use default commit message if not provided
            if not git_message:
                now = datetime.datetime.now()
                git_message = f"Auto-commit at {now.strftime('%Y-%m-%d %H:%M:%S')}"

            # Commit changes
            repo.index.commit(git_message)
            logger.info(f"Committed changes with message: '{git_message}'")

            # Push changes to remote repository
            origin = repo.remote(name="origin")
            origin.push(branch)
            logger.info(f"Successfully pushed changes to branch '{branch}' for repository '{dirfile}'")

        except GitCommandError as e:
            logger.error(f"Git command error in repository '{dirfile}': {e}")
        except Exception as e:
            logger.error(f"Unexpected error in repository '{dirfile}': {e}")


if __name__ == "__main__":

    git_paths = r"""D:\Github\0MyApp\AudioProcess main
D:\Github\0MyApp\AutoPublishVideo main
D:\Github\0MyApp\GitAutoPush main
D:\Github\0MyApp\ImgProcess main
D:\Github\0MyApp\UpdateSubtitle main
D:\Github\0MyApp\WhisperWebUI main
D:\Github\0MyApp\YTBDL main
"""
    git_auto_push(git_paths)

