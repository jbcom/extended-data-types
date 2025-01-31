"""Git repository operations and utilities."""

from __future__ import annotations

import tempfile

from pathlib import Path

from git import GitCommandError, InvalidGitRepositoryError, NoSuchPathError, Repo

from .types import FilePath


def get_parent_repository(
    file_path: FilePath | None = None, search_parent_directories: bool = True
) -> Repo | None:
    """Get Git repository containing the given path.

    Args:
        file_path: Path within repository (default: current directory)
        search_parent_directories: Whether to search parent directories

    Returns:
        Git repository if found, None otherwise
    """
    directory = Path(str(file_path)) if file_path else Path.cwd()

    try:
        return Repo(str(directory), search_parent_directories=search_parent_directories)
    except (InvalidGitRepositoryError, NoSuchPathError):
        return None


def get_repository_name(repo: Repo) -> str | None:
    """Get name of Git repository from remote URL.

    Args:
        repo: Git repository instance

    Returns:
        Repository name if available, None otherwise
    """
    try:
        remote_url = next(iter(repo.remotes[0].urls))
        return Path(remote_url).stem
    except (IndexError, ValueError, StopIteration):
        return None


def clone_repository_to_temp(
    repo_owner: str, repo_name: str, github_token: str, branch: str | None = None
) -> tuple[Path, Repo]:
    """Clone GitHub repository to temporary directory.

    Args:
        repo_owner: Repository owner/organization
        repo_name: Repository name
        github_token: GitHub access token
        branch: Branch to clone (default: default branch)

    Returns:
        Tuple of (temp directory path, repository instance)

    Raises:
        OSError: If clone fails
    """
    repo_url = (
        f"https://{github_token}:x-oauth-basic@github.com/{repo_owner}/{repo_name}.git"
    )

    try:
        temp_dir = Path(tempfile.mkdtemp())
        repo = Repo.clone_from(repo_url, str(temp_dir), branch=branch)
        return temp_dir, repo
    except GitCommandError as e:
        raise OSError("Git command error occurred") from e
    except InvalidGitRepositoryError as e:
        raise OSError("Invalid or corrupt repository") from e
    except NoSuchPathError as e:
        raise OSError("Path does not exist") from e
    except PermissionError as e:
        raise OSError("Permission denied: Check GitHub token and permissions") from e


def get_repository_root(
    file_path: FilePath | None = None, search_parent_directories: bool = True
) -> Path | None:
    """Get root directory of Git repository.

    Args:
        file_path: Path within repository (default: current directory)
        search_parent_directories: Whether to search parent directories

    Returns:
        Repository root path if found, None otherwise
    """
    repo = get_parent_repository(file_path, search_parent_directories)
    if repo and repo.working_tree_dir:
        return Path(repo.working_tree_dir)
    return None
