##Read me working setup for custom cli

Step-by-Step Guide to Setting Up Your Custom groq-cli

##################################################
Step 1: Prepare Your Project Directory Structure
Recommended structure:

groq_cli_package/
  pyproject.toml
  groq_cli.py

##################################################
Step 2: Write/Edit pyproject.toml
Copy this into pyproject.toml in your folder:

----------------------------------------------Copy below exactly in .toml file-----------------------
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
----------------------------------------------------------------------------------------------------
Add more dependencies as you need.

###############################################
Step 3: Put Your Code in groq_cli.py
Your CLI code (must expose a main() function).

a. Copy the entire groq_cli.py code inside your .py file
b. Always ensure at the bottom the below command is present:
----------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
----------------------------------------------------------------------------------------------------

##################################################
Step 4: Set your API Keys as Environment Variables

a. Open shell file called zshrc file from your macbook terminal: type "vim ~/.zshrc"
b. Paste the below code inside shell file from your terminal(for macbook terminal the file will be ~/.zshrc, for windows terminal it will mostly be ~/.bash shell but verify it):
---------------------------------------------------------------------------------------------------
export GOOGLE_CLOUD_PROJECT="YOUR_GOOGLE_PROJECT_ID"
export PATH="$PATH:/Users/YOUR_LAPTOP_USERID/.local/bin"
export PATH="$HOME/.local/bin:$PATH"
export GROQ_API_KEY="API_KEY_FROM_GROQ_DEVELOPER_PLATFORM"
export PERPLEXITY_API_KEY="PERPLEXITY_PLATFORM_API_KEY"
export GOOGLE_API_KEY="GOOGLE_API_KEY_FROM_SAME_PROJECT_ID"
export GOOGLE_CSE_ID="GOOGLE_MAPS_API_KEY_FROM_SAME_PROJECT_ID"
---------------------------------------------------------------------------------------------------
c. Once the above lines are apsted inside the shell file(~/.zshrc file) then activate(bring in effect of new changes), run below command in terminal 
"source ~/.zshrc"

#################################################
Step 5: Set Up pipx if not installed before
a. Type below commands in the terminal
-------------------------------------------------------------------------------------------------
python3 -m pip install --user pipx
python3 -m pipx ensurepath
-------------------------------------------------------------------------------------------------

b.Restart terminal or open a fresh new terminal session(always perform this action to take effect of any new changes to shell file)

#################################################
Step 6: Install Your CLI via pipx
a. Enter the same directory as your groq_cli_package directory(ensure there are no other files or folder apart from the github pulled files):

b. Enter the below command to activate it(for first time setup)
-------------------------------------------------------------------------------------------------
pipx install .
-------------------------------------------------------------------------------------------------
This installs all dependencies automatically in a self-contained venv.

Step 7: Run Your CLI
a. From any directory inside the terminal, just type below in your terminal:
-------------------------------------------------------------------------------------------------
groq-cli
-------------------------------------------------------------------------------------------------
Choose your LLM, chat, use /search ... for web search.

################################################
Step 8:  For any updation of python files/ adding New Packages, changing of environment variables
a. To update code: Edit groq_cli.py or other relevant files.

b. Then run either of a1 or a2:
-------------------------------------------------------------------------------------------------
a1: pipx reinstall groq-cli or 

Run the below 2 commands in case the above fails or cli is not starting(this delete's and reinstalls cleanly always, also is preferred option)
a2: pipx uninstall groq-cli
    pipx install .
-------------------------------------------------------------------------------------------------

c. To add new dependencies of packages:
Edit your pyproject.toml:
-------------------------------------------------------------------------------------------------
dependencies = [
    "groq",
    "requests",
    "rich"
]
-------------------------------------------------------------------------------------------------
Then run either a1 or a2(preferred):

The new package is now installed and ready to use.



################# NOTE ######################
### Any changes made to the python code / changes or updates to ~/.zshrc file for the environment variables 
1. Open a new terminal alwasys. This reloads the environment variables to take into account any new changes to environment vairables
2. Run: pipx uninstall groq-cli, pipx install .
3. Then finally run terminal cli command ex: groq-cli



Full Checklist Table Structure(Highlight)
Step	Command/File	What it’s for
Setup	Structure as above	Project layout
deps	Edit pyproject.toml	Manage dependencies + script
code	Code in groq_cli.py	Main CLI logic
keys	Add API keys in ~/.zshrc	Auth for Groq/Perplexity
install	pipx install .	Install CLI (one step)
update	pipx reinstall groq-cli	Apply code/dependency updates

Use only pyproject.toml for dependencies—no requirements.txt needed!

Upgrades are seamless with pipx reinstall groq-cli

Add new packages ONLY in pyproject.toml and use the reinstall command.
