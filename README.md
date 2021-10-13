# ORNL Domex Pipeline
[![Tests](https://github.com/UNCWMixedReality/ORNLDOMEXPipeline/actions/workflows/build.yml/badge.svg)](https://github.com/UNCWMixedReality/ORNLDOMEXPipeline/actions/workflows/build.yml)

A python pipeline to allow the extraction of text from a variety of file types, and subsequent classification of the extracted text

### Initial development setup
This repository utilizes the pre-commit library for linting and styling, it also uses docker and docker-compose for ease of development across devices. To set up your machine for this project, please perform the following steps:
1. Ensure that [docker](https://docker.com) is installed on your machine
2. Ensure that [docker-compose](https://docs.docker.com/compose/install/) is also installed on your machine
3. Ensure that Python3.5 or greater is installed on your machine
4. Clone the repository on your local machine
5. Initialize and activate a virtual environment the repository

```bash
# Windows
python -m venv env && .\env\scripts\activate.bat

# *nix
python3 -m venv env && source env/bin/activate
```

5. Install the projects requirements

`pip install -r requirements.txt`

6. Configure your git repository with the necessary pre-commit hooks

`pre-commit install`

### Pushing changes
This repository follows a simplified version of the git branching guidelines found in [this article](https://nvie.com/posts/a-successful-git-branching-model/). The **main** branch strives to always contain a stable build. **development** will contain the current version of the project that is in active development. New features should be branch off of **development** and follwing the naming scheme of **feature/{feature description}**. 

Merges into **development** will go through code-review, and should build in docker, but don't worry too much about that as we'll work through those changes during the code review.

### Spinning up in docker-compose
To launch the project in docker-compose for local development, navigate to the root of the repository and run the following command:

`docker-compose up -d`

To see how the project is tested in the continuos integration pipeline (Github Actions), run with the folliwng command:

`docker-compose --file ./ci/docker-compose.yml up -d`

Note that the CI pipeline may expect environment variables or secrets that are not available to your local machine, which may cause failures during this process.