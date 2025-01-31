"""Tests for Git repository operations."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from extended_data_types.io.git import (
    clone_repository_to_temp,
    get_parent_repository,
    get_repository_name,
    get_repository_root,
)
from git import GitCommandError, InvalidGitRepositoryError, NoSuchPathError, Repo


@pytest.fixture()
def mock_repo():
    """Create a mock Git repository."""
    repo = Mock(spec=Repo)
    repo.working_tree_dir = "/mock/repo/path"
    remote = Mock()
    remote.urls = iter(["https://github.com/owner/repo-name.git"])
    repo.remotes = [remote]
    return repo


class TestGetParentRepository:
    """Tests for get_parent_repository function."""

    def test_current_directory(self, mock_repo):
        """Test getting repository from current directory."""
        with patch("git.Repo") as mock_git_repo:
            mock_git_repo.return_value = mock_repo
            result = get_parent_repository()
            assert result == mock_repo
            mock_git_repo.assert_called_once()

    def test_specific_path(self, mock_repo):
        """Test getting repository from specific path."""
        with patch("git.Repo") as mock_git_repo:
            mock_git_repo.return_value = mock_repo
            result = get_parent_repository("/some/path")
            assert result == mock_repo
            mock_git_repo.assert_called_once_with(
                "/some/path", search_parent_directories=True
            )

    def test_not_git_repo(self):
        """Test handling of non-Git repository."""
        with patch("git.Repo", side_effect=InvalidGitRepositoryError):
            assert get_parent_repository("/not/a/repo") is None

    def test_nonexistent_path(self):
        """Test handling of nonexistent path."""
        with patch("git.Repo", side_effect=NoSuchPathError):
            assert get_parent_repository("/does/not/exist") is None


class TestGetRepositoryName:
    """Tests for get_repository_name function."""

    def test_valid_repo(self, mock_repo):
        """Test getting name from valid repository."""
        assert get_repository_name(mock_repo) == "repo-name"

    def test_no_remotes(self):
        """Test handling of repository without remotes."""
        repo = Mock(spec=Repo)
        repo.remotes = []
        assert get_repository_name(repo) is None

    def test_invalid_remote_url(self):
        """Test handling of invalid remote URL."""
        repo = Mock(spec=Repo)
        remote = Mock()
        remote.urls = iter(["invalid://url"])
        repo.remotes = [remote]
        assert get_repository_name(repo) == "url"


class TestCloneRepositoryToTemp:
    """Tests for clone_repository_to_temp function."""

    @patch("tempfile.mkdtemp")
    @patch("git.Repo.clone_from")
    def test_successful_clone(self, mock_clone, mock_mkdtemp, mock_repo):
        """Test successful repository cloning."""
        mock_mkdtemp.return_value = "/tmp/test"
        mock_clone.return_value = mock_repo

        temp_dir, repo = clone_repository_to_temp("owner", "repo", "token123", "main")

        assert temp_dir == Path("/tmp/test")
        assert repo == mock_repo
        mock_clone.assert_called_once_with(
            "https://token123:x-oauth-basic@github.com/owner/repo.git",
            "/tmp/test",
            branch="main",
        )

    @pytest.mark.parametrize(
        "exception,expected_message",
        [
            (GitCommandError("cmd", 1), "Git command error occurred"),
            (InvalidGitRepositoryError, "Invalid or corrupt repository"),
            (NoSuchPathError, "Path does not exist"),
            (PermissionError, "Permission denied: Check GitHub token and permissions"),
        ],
    )
    def test_clone_errors(self, exception, expected_message):
        """Test handling of various clone errors."""
        with patch("git.Repo.clone_from", side_effect=exception):
            with pytest.raises(OSError, match=expected_message):
                clone_repository_to_temp("owner", "repo", "token")


class TestGetRepositoryRoot:
    """Tests for get_repository_root function."""

    def test_valid_repo(self, mock_repo):
        """Test getting root from valid repository."""
        with patch("git.Repo") as mock_git_repo:
            mock_git_repo.return_value = mock_repo
            result = get_repository_root("/some/path")
            assert result == Path("/mock/repo/path")

    def test_no_working_tree(self):
        """Test handling of repository without working tree."""
        repo = Mock(spec=Repo)
        repo.working_tree_dir = None
        with patch("git.Repo") as mock_git_repo:
            mock_git_repo.return_value = repo
            assert get_repository_root("/some/path") is None

    def test_not_git_repo(self):
        """Test handling of non-Git repository."""
        with patch("git.Repo", side_effect=InvalidGitRepositoryError):
            assert get_repository_root("/not/a/repo") is None
