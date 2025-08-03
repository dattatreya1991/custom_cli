import os
import sys
import requests
import json
from groq import Groq

# ANSI Colors (unchanged)
BOLD        = '\033[1m'
RESET       = '\033[0m'
CYAN        = '\033[36m'
BRIGHT_CYAN = '\033[96m'
SILVER      = '\033[37m'
GRAY        = '\033[90m'
LIGHT_GRAY  = '\033[38;5;250m'
YELLOW      = '\033[93m'
GREEN       = '\033[92m'
WHITE       = '\033[97m'
ERROR       = '\033[91m'

PROMPT_COLOR = CYAN
MODEL_COLOR  = YELLOW

AVAILABLE_MODELS = [
    ("llama-3.3-70b-versatile", "Llama 3.3 70B Versatile"),
    ("qwen/qwen3-32b", "Qwen 3 32B"),
    ("moonshotai/kimi-k2-instruct", "Kimi k2 Instruct"),
]

def select_model():
    print("\nSelect a model to use (type anything from the name or model ID):")
    for i, (model_id, desc) in enumerate(AVAILABLE_MODELS, 1):
        print(f"  {i}. {desc} ({model_id})")
    while True:
        choice = input("Enter model (name, ID, or number): ").strip().lower()
        if choice.isdigit():
            n = int(choice)
            if 1 <= n <= len(AVAILABLE_MODELS):
                return AVAILABLE_MODELS[n - 1][0]
        for model_id, desc in AVAILABLE_MODELS:
            if choice == model_id.lower():
                return model_id
        matches = [model_id for model_id, desc in AVAILABLE_MODELS
                   if choice in model_id.lower() or choice in desc.lower()]
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            print("Multiple matches found:")
            for m in matches:
                print(f"  - {m}")
            print("Please be more specific.")
        else:
            print("Model not recognized. Try any part of the name/ID or the number.")

def print_colored_response(text):
    lines = text.split('\n')
    in_code_block = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            print(GREEN + line + RESET)
        elif in_code_block:
            print(GREEN + line + RESET)
        else:
            print(GRAY + line + RESET)

def perplexity_search(query, api_key, model="sonar-pro"):
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": query}
        ],
        "enable_search_classifier": True
    }
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code != 200:
        return None, f"Perplexity error: {r.status_code} {r.text}"
    data = r.json()
    return data, None

def google_search(query, api_key, cse_id, num=3):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
        "num": num
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return None, f"Google error: {r.status_code} {r.text}"
    data = r.json()
    return data, None

def list_all_files(root="."):
    for dirpath, dirnames, filenames in os.walk(root):
        level = dirpath.replace(root, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{BRIGHT_CYAN}{indent}{os.path.basename(dirpath)}/ {RESET}")
        subindent = ' ' * 4 * (level + 1)
        for f in filenames:
            print(f"{subindent}{GRAY}{f}{RESET}")

def read_file(filename):
    try:
        if not os.path.isfile(filename):
            print(f"{ERROR}File not found: {filename}{RESET}")
            return
        if filename.endswith(".ipynb"):
            with open(filename, "r", encoding="utf-8") as f:
                nb = json.load(f)
            code_cells = []
            for cell in nb.get("cells", []):
                if cell.get("cell_type") == "code":
                    code = "".join(cell.get("source", []))
                    code_cells.append(code)
            code_combined = "\n\n".join(code_cells)
            print(f"{BOLD}{CYAN}Code extracted from {filename}:{RESET}\n")
            print_colored_response(code_combined if code_combined else "[No code found in notebook]")
        else:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            print(f"{BOLD}{CYAN}File: {filename}{RESET}\n")
            print_colored_response(content)
    except Exception as e:
        print(f"{ERROR}Error reading file {filename}: {e}{RESET}")

def analyze_file(filename, llm_client, model):
    try:
        if not os.path.isfile(filename):
            print(f"{ERROR}File not found: {filename}{RESET}")
            return

        # Extract relevant content to analyze
        if filename.endswith(".ipynb"):
            with open(filename, "r", encoding="utf-8") as f:
                nb = json.load(f)
            code_cells = []
            for cell in nb.get("cells", []):
                if cell.get("cell_type") == "code":
                    code = "".join(cell.get("source", []))
                    code_cells.append(code)
            code_combined = "\n\n".join(code_cells)
            if not code_combined:
                print(f"{ERROR}No code found in notebook.{RESET}")
                return
            content_to_check = code_combined
        else:
            with open(filename, "r", encoding="utf-8") as f:
                content_to_check = f.read()

        print(f"{CYAN}Analyzing {filename} for errors using the selected model. Please wait...{RESET}")
        system_prompt = "You are a code review assistant. The following is a file content. Identify any problems, errors, or suspicious code, and suggest improvements if needed."
        user_prompt = f"File content:\n{content_to_check}"

        response = llm_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )
        print(f"{GREEN}Analysis Report:{RESET}")
        print_colored_response(response.choices[0].message.content)
    except Exception as e:
        print(f"{ERROR}Error analyzing file: {e}{RESET}")

def main():
    api_key = os.environ.get("GROQ_API_KEY")
    perplexity_api_key = os.environ.get("PERPLEXITY_API_KEY")
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    google_cse_id = os.environ.get("GOOGLE_CSE_ID")
    
    if not api_key:
        print("Error: GROQ_API_KEY environment variable not set.")
        sys.exit(1)
    client = Groq(api_key=api_key)
    model = select_model()
    print(f"\n{PROMPT_COLOR}{BOLD}Groq CLI Interactive Chat{RESET} [{MODEL_COLOR}{model}{RESET}]. Type 'exit' or Ctrl+C to quit.")
    print("Type /list to list files and folders.")
    print("Type /read <filename> to display a file (extracts code from .ipynb).")
    print("Type /analyze <filename> for LLM code analysis/error detection.")
    print("Type /model <model_name/id/number/keyword> any time to switch models.")
    print("Type /search [google|perplexity] <your query> for web search.\n")
    try:
        while True:
            prompt = input(f"{PROMPT_COLOR}{BOLD}groq-cli [{model}]{RESET} > ")
            if prompt.strip().lower() in ("exit", "quit"):
                break

            # --------- List directory section ---------
            if prompt.strip().lower().startswith("/list"):
                print(f"{CYAN}Recursive file/directory listing from current directory:{RESET}")
                list_all_files(".")
                continue

            # --------- Read file section -------------
            if prompt.strip().lower().startswith("/read "):
                filename = prompt.strip()[6:].strip()
                read_file(filename)
                continue

            # --------- Analyze file section ----------
            if prompt.strip().lower().startswith("/analyze "):
                filename = prompt.strip()[9:].strip()
                analyze_file(filename, client, model)
                continue

            # --------- Flexible Search Section ---------
            if prompt.strip().lower().startswith("/search"):
                parts = prompt.strip().split(maxsplit=2)
                if len(parts) < 2:
                    print("Usage: /search [google|perplexity] <query>")
                    continue
                if len(parts) == 2:
                    search_source = "perplexity"
                    search_query = parts[1]
                else:
                    search_source = parts[1].lower()
                    search_query = parts[2]
                if not search_query:
                    print("Usage: /search [google|perplexity] <your query>")
                    continue
                if search_source == "google":
                    if not google_api_key or not google_cse_id:
                        print(f"{ERROR}Google API/CSE key missing! Set GOOGLE_API_KEY and GOOGLE_CSE_ID env variables.{RESET}")
                        continue
                    print(f"{BOLD}{CYAN}Searching Google for:{RESET} {search_query}")
                    data, err = google_search(search_query, google_api_key, google_cse_id)
                    if err:
                        print(f"{ERROR}{err}{RESET}")
                        continue
                    items = data.get("items", [])
                    if items:
                        for idx, item in enumerate(items, 1):
                            title = item.get("title", "")
                            link = item.get("link", "")
                            snippet = item.get("snippet", "")
                            print(f"{BOLD}{YELLOW}Result {idx}:{RESET} {title}\n  {BRIGHT_CYAN}{link}{RESET}\n  {GRAY}{snippet}{RESET}\n")
                        # -- AI summary from top snippets --
                        summarize_input = "\n".join(f"{item.get('title','')}: {item.get('snippet','')}" for item in items[:3])
                        system_prompt = "Summarize these Google Search results to a concise answer based only on their combined facts."
                        try:
                            summary_response = client.chat.completions.create(
                                model=model,
                                messages=[
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": summarize_input}
                                ],
                            )
                            print(f"{GREEN}AI Summary:{RESET}")
                            print_colored_response(summary_response.choices[0].message.content)
                        except Exception as summarize_error:
                            print(f"{ERROR}Summary error: {summarize_error}{RESET}")                        
                    else:
                        print(f"{ERROR}No results from Google.{RESET}")
                    continue
                elif search_source == "perplexity":
                    if not perplexity_api_key:
                        print(f"{ERROR}Perplexity API key missing! Set PERPLEXITY_API_KEY env variable.{RESET}")
                        continue
                    print(f"{BOLD}{CYAN}Searching Perplexity for:{RESET} {search_query}")
                    data, err = perplexity_search(search_query, perplexity_api_key, model="sonar-pro")
                    if err:
                        print(f"{ERROR}{err}{RESET}")
                        continue
                    if data is not None and "choices" in data and data["choices"]:
                        for choice in data["choices"]:
                            content = choice.get("message", {}).get("content", "")
                            print(f"{BOLD}{YELLOW}Perplexity result:{RESET}\n{content}\n")
                        if data.get("citations"):
                            print(f"{CYAN}Citations:{RESET}")
                            for url in data["citations"]:
                                print(f"{BRIGHT_CYAN}{url}{RESET}")
                        if data.get("search_results"):
                            print(f"{CYAN}Search Results:{RESET}")
                            for res in data["search_results"]:
                                title = res.get("title", "(no title)")
                                url = res.get("url", "(no url)")
                                print(f"- {title} {BRIGHT_CYAN}{url}{RESET}")
                    else:
                        print(f"{ERROR}No results from Perplexity.{RESET}")
                    continue
                else:
                    print("Usage: /search [google|perplexity] <your query>")
                    continue

            # --------- Model Switching Section ---------
            if prompt.strip().startswith("/model"):
                parts = prompt.strip().split(maxsplit=1)
                if len(parts) == 2:
                    new_choice = parts[1].strip().lower()
                    if new_choice.isdigit():
                        n = int(new_choice)
                        if 1 <= n <= len(AVAILABLE_MODELS):
                            model = AVAILABLE_MODELS[n - 1][0]
                            print(f"Switched to model: {model}")
                            continue
                    for model_id, desc in AVAILABLE_MODELS:
                        if new_choice == model_id.lower():
                            model = model_id
                            print(f"Switched to model: {model}")
                            break
                    else:
                        matches = [model_id for model_id, desc in AVAILABLE_MODELS
                                   if new_choice in model_id.lower() or new_choice in desc.lower()]
                        if len(matches) == 1:
                            model = matches[0]
                            print(f"Switched to model: {model}")
                            continue
                        elif len(matches) > 1:
                            print("Multiple matches found:")
                            for m in matches:
                                print(f"  - {m}")
                            print("Please be more specific.")
                            continue
                        else:
                            print("Model not recognized. Try a name, ID, or number.")
                            continue
                else:
                    print("Usage: /model <model_name/id/number/keyword>")
                    continue
            # --------- LLM Query as before ---------
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                )
                print(f"{GREEN}Groq:{RESET}")
                print_colored_response(response.choices[0].message.content)
            except Exception as e:
                print(f"{ERROR}Groq error: {e}{RESET}")
    except KeyboardInterrupt:
        print("\nExiting Groq CLI.")

if __name__ == "__main__":
    main()

