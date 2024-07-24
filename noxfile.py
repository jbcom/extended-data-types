import tempfile
import nox
from nox_poetry import session

# Specify the Python versions to test
python_versions = ["3.8", "3.9", "3.10", "3.11", "3.12"]

# List of dependencies for the tests
test_dependencies = [
    "pytest",
    "pytest-mock",
    "pytest-asyncio",
    "coverage[toml]",
]


@nox.session(python=python_versions)
def tests(session):
    # Install dependencies specified in poetry.lock
    session.install(".")
    session.install(*test_dependencies)

    # Logging installed packages
    session.log("Installed packages:")
    session.run("pip", "list")

    # Run tests with coverage
    session.run("coverage", "run", "-m", "pytest", *session.posargs)


@nox.session(python="3.12")
def coverage_report(session):
    # Install coverage
    session.install("coverage[toml]")

    # Combine coverage data and generate the report
    session.run("coverage", "combine")
    session.run("coverage", "report")


@nox.session(python="3.12")
def docs(session):
    # Install documentation dependencies
    session.install("sphinx", "sphinx-rtd-theme", "sphinx-markdown-builder")

    # Logging installed packages
    session.log("Installed packages for docs:")
    session.run("pip", "list")

    # Create a temporary directory for Sphinx doctrees
    with tempfile.TemporaryDirectory() as tmpdir:
        # Build the documentation
        session.run("sphinx-build", "-n", "-T", "-W", "-b", "html", "-d", f"{tmpdir}/doctrees", "docs",
                    "docs/_build/html")
