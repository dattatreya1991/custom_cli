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


###################################################################################################



########### Common Model choices & cmmon tasks with its command ########## 
a. The below are the actual 3 models available for use(actual dsiplayed indo from the cli):-

Select a model to use (type anything from the name or model ID):
  1. Llama 3.3 70B Versatile (llama-3.3-70b-versatile)
  2. Qwen 3 32B (qwen/qwen3-32b)
  3. Kimi k2 Instruct (moonshotai/kimi-k2-instruct)
Enter model (name, ID, or number): type either </1>, </kimi> or </llama> etc

b. The below are the actual displayed commands possible in the cli:-

Groq CLI Interactive Chat [llama-3.3-70b-versatile]. Type 'exit' or Ctrl+C to quit.
-) Type /list [dir] to list files/folders (optionally from a certain directory).
-) Type /read <filename> to display a file (extracts code from .ipynb).
-) Type /analyze <filename> for LLM code analysis/error detection.
-) Type /model <model_name/id/number/keyword> any time to switch models.
-) Type /search [google|perplexity] <your query> for web search.
-)Type /write <outputfile.py|.txt> <instruction with input filename> to generate new code/text and save output to a file (.txt/.py).

Example: 
-) groq-cli [llama-3.3-70b-versatile] > /write groq_updated_code.py Make improvements to the code in groq_cli.py and write the entire updated code only to the file. 	# Read a file, make updates to the code and write it to another file
-) groq-cli [llama-3.3-70b-versatile] > /list									# list all the files inside the current directory from which groq-cli was started
-) groq-cli [llama-3.3-70b-versatile] > /read groq_cli.py							# Reading contents and printing
-) groq-cli [llama-3.3-70b-versatile] > /analyze groq_cli.py							# Understands the file/code and provides basic suggestions overview
-) groq-cli [llama-3.3-70b-versatile] > /model 1								# Model switching
-) groq-cli [llama-3.3-70b-versatile] > /model kimi								# Model switching
-) groq-cli [llama-3.3-70b-versatile] > /search perplexity Search and summarise latest Ai trends in 2025	# Search perplexity(better search since it summarises the results )
-) groq-cli [llama-3.3-70b-versatile] > /search google Search and summarise latest Ai trends in 2025		# Search Google(only provides links to search results)




To auto-write a response, append '> filename.txt' or '> filename.py' to your question.










##########################################################################

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

