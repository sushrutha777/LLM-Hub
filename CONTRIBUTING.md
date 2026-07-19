# Contributing to LLMHub

First off, thank you for considering contributing to LLMHub! It's people like you that make LLMHub a great open-source platform.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/LLM-Hub.git`
3. Check out a new branch: `git checkout -b feature/your-feature-name`

## Development Workflow

- **Architecture:** We follow a Microservices Architecture based on Clean Architecture principles. Please review `docs/ARCHITECTURE.md` before making structural changes.
- **Testing:** Add tests for any new features in the respective `tests/` directory of the microservice.
- **Type Hints:** All Python code must include type hints.
- **Documentation:** If you add a new endpoint, please update `docs/api/`.

## Pull Request Process

1. Ensure your code passes all local linting and tests.
2. Update the README.md or docs with details of changes to the interface, if applicable.
3. Use the provided Pull Request Template.
4. Once your PR is submitted, it will trigger the GitHub Actions CI pipeline. A maintainer will review it shortly.

## Community

Join the discussion in our GitHub Discussions or Issues!
