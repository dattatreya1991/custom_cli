##Read me working setup for custom cli

Step-by-Step Guide to Setting Up Your Custom groq-cli

##################################################
Step 1: Prepare Your Project Directory Structure
Recommended structure:

custom_groq_cli/
	requirements.txt
  	Readme.txt
  	MANIFEST.in
  	pyproject.toml
  	groq_cli_package/
		models.json
		models.py
		__init__.py
		groq_cli.py
	

##################################################
Step 2: Write/Edit pyproject.toml
Copy this into pyproject.toml in your folder:

----------------------------------------------Copy below exactly in .toml file-----------------------
[project]
name = "groq-cli"
version = "0.1.0"
description = "Groq CLI"
requires-python = ">=3.8"
dependencies = ["groq", "requests"]

[project.scripts]
groq-cli = "groq_cli_package.groq_cli:main"

[tool.setuptools]
include-package-data = true

[tool.setuptools.packages.find]
where = ["."]

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
    "new_dependency"
]
-------------------------------------------------------------------------------------------------
Then run either a1 or a2(preferred):

#########################################################################################################################



########################################################### NOTE ########################################################
########### Examples & Usage: Common Model choices & common tasks with its command ########## 

a. The below are the actual 3 models available for use(actual dsiplayed indo from the cli):-

Select a model to use (type anything from the name or model ID):
  1. Llama 3.3 70B Versatile (llama-3.3-70b-versatile)
  2. Qwen 3 32B (qwen/qwen3-32b)
  3. Kimi k2 Instruct (moonshotai/kimi-k2-instruct)
Enter model (name, ID, or number): type either </1>, </kimi> or </llama> etc. (New models can be added and this option can change slightly, take this example as a reference)

b. The below are the actual displayed commands possible in the cli:-

Groq CLI Interactive Chat [llama-3.3-70b-versatile]. Type 'exit' or Ctrl+C to quit.
-) Type /list [dir] to list files/folders (optionally from a certain directory).
-) Type /read <filename> to display a file (extracts code from .ipynb).
-) Type /analyze <filename> for LLM code analysis/error detection.
-) Type /model <model_name/id/number/keyword> any time to switch models.
-) Type /search [google|perplexity] <your query> for web search.
-)Type /write <outputfile.py|.txt> <instruction with input filename> to generate new code/text and save output to a file (.txt/.py).

Example: 
-) groq-cli [llama-3.3-70b-versatile] > /write groq_updated_code.py Make improvements to the code in groq_cli.py and write the entire updated code only to the file. 	# Read a file, make updates to 
-) groq-cli [llama-3.3-70b-versatile] > /list									# list all the files inside the current directory from which groq-cli was started
-) groq-cli [llama-3.3-70b-versatile] > /read groq_cli.py							# Reading contents and printing
-) groq-cli [llama-3.3-70b-versatile] > /analyze groq_cli.py							# Understands the file/code and provides basic suggestions overview
-) groq-cli [llama-3.3-70b-versatile] > /model 1								# Model switching
-) groq-cli [llama-3.3-70b-versatile] > /model kimi								# Model switching
-) groq-cli [llama-3.3-70b-versatile] > /search perplexity Search and summarise latest Ai trends in 2025	# Search perplexity(better search since it summarises the results )
-) groq-cli [llama-3.3-70b-versatile] > /search google Search and summarise latest Ai trends in 2025		# Search Google(only provides links to search results)


To auto-write a response, append '> filename.txt' or '> filename.py' to your question.

########################################################################################################################################


######### Any changes made to the python code / changes or updates to ~/.zshrc file for the environment variables 
1. Open a new terminal alwasys. This reloads the environment variables to take into account any new changes to environment vairables
2. Run: pipx uninstall groq-cli, pipx install .
3. Then finally run terminal cli command ex: groq-cli

Use only pyproject.toml for dependencies—no requirements.txt needed!

Upgrades are seamless with pipx reinstall groq-cli

Add new packages ONLY in pyproject.toml and use the reinstall command.
