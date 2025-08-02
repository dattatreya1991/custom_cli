##Read me working setup for custom cli

Step-by-Step Guide to Setting Up Your Custom groq-cli


Step 1: Prepare Your Project Directory Structure
Recommended structure:

text
groq_cli_package/
  pyproject.toml
  groq_cli.py


Step 2: Write/Edit pyproject.toml
Copy this into pyproject.toml in your folder:

text
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "groq-cli"
version = "0.1.0"
description = "Groq CLI with Perplexity Search"
requires-python = ">=3.8"
dependencies = [
    "groq",
    "requests"
]
[project.scripts]
groq-cli = "groq_cli:main"
Add more dependencies as you need (e.g., "rich").

Step 3: Put Your Code in groq_cli.py
Your CLI code (must expose a main() function).

At bottom:

python
if __name__ == "__main__":
    main()
Step 4: Set your API Keys as Environment Variables
In your terminal:

text
echo 'export GROQ_API_KEY="your_groq_api_key"' >> ~/.zshrc
echo 'export PERPLEXITY_API_KEY="your_perplexity_api_key"' >> ~/.zshrc
source ~/.zshrc
Step 5: Set Up pipx if not installed
text
python3 -m pip install --user pipx
python3 -m pipx ensurepath
# Restart terminal
Step 6: Install Your CLI via pipx
From your groq_cli_package directory:

text
pipx install .
This installs all dependencies automatically in a self-contained venv.

Step 7: Run Your CLI
Anywhere, just type:

text
groq-cli
Choose your LLM, chat, use /search ... for web search.

Step 8: UPDATING and Adding New Packages
To update code:
Edit groq_cli.py or other relevant files.

Then run:

text
pipx reinstall groq-cli
To add new dependencies (e.g. rich):
Edit your pyproject.toml:

text
dependencies = [
    "groq",
    "requests",
    "rich"
]
Then run:

text
pipx reinstall groq-cli
The new package is now installed and ready to use.



################# NOTE ######################
### Any changes made to the python code / changes or updates to ~/.zshrc file for the environment variables 
1. Open a new terminal alwasys. This reloads the environment variables to take into account any new changes to environment vairables
2. Run: pipx uninstall groq-cli, pipx install .
3. Then finally run terminal cli command ex: groq-cli



Full Checklist Table
Step	Command/File	What it’s for
Setup	Structure as above	Project layout
deps	Edit pyproject.toml	Manage dependencies + script
code	Code in groq_cli.py	Main CLI logic
keys	Add API keys in ~/.zshrc	Auth for Groq/Perplexity
install	pipx install .	Install CLI (one step)
update	pipx reinstall groq-cli	Apply code/dependency updates
Summary
Use only pyproject.toml for dependencies—no requirements.txt needed!

Upgrades are seamless with pipx reinstall groq-cli

Add new packages ONLY in pyproject.toml and use the reinstall command.

This is the “one-command” robust method and the only one needed with modern pipx+Python packaging.
Let me know if you need a full template pyproject.toml or example main code!

