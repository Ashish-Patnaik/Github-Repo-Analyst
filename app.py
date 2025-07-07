import os
import re
import asyncio
import streamlit as st
from github import Github, GithubException

# --- Configuration & Setup ---

st.set_page_config(
    page_title="GitHub Repo Analyst",
    page_icon="1.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Helper Functions (No changes here) ---

def validate_repo_url(url: str) -> str:
    """Validate and extract owner/repo from a GitHub URL."""
    pattern = r"https?://github\.com/([^/]+)/([^/]+)"
    match = re.match(pattern, url)
    if not match:
        raise ValueError("Invalid GitHub URL. Please use the format: https://github.com/owner/repo")
    return f"{match.group(1)}/{match.group(2)}"

def get_important_file_content(repo, max_files=7, max_file_size=15000):
    """Fetches content from important files in the repository to provide context to the LLM."""
    priority_files = [
        "README.md", "pyproject.toml", "package.json", "requirements.txt",
        "main.py", "app.py", "index.js", "docker-compose.yml", "Dockerfile",
        "pom.xml", "build.gradle"
    ]
    file_contents = {}
    try:
        contents = repo.get_contents("")
        files_to_check = [f for f in contents if f.type == 'file']
        files_to_check.sort(key=lambda f: priority_files.index(f.name) if f.name in priority_files else float('inf'))
        for content_file in files_to_check[:max_files]:
            if content_file.size > max_file_size:
                file_contents[content_file.path] = f"--- File content too large (>{max_file_size} bytes) ---"
                continue
            try:
                decoded_content = content_file.decoded_content.decode('utf-8')
                file_contents[content_file.path] = decoded_content
            except (UnicodeDecodeError, GithubException):
                file_contents[content_file.path] = "--- Could not decode file content ---"
    except GithubException as e:
        st.warning(f"Could not fetch some file contents: {e}")
    return file_contents

def fetch_repo_data(g: Github, repo_name: str) -> dict:
    """Fetch comprehensive repository metadata and content using the GitHub API."""
    try:
        repo = g.get_repo(repo_name)
        languages = repo.get_languages()
        tech_stack = list(languages.keys())
        important_files = get_important_file_content(repo)
        return {
            "name": repo.name, "owner": repo.owner.login,
            "description": repo.description or "No description provided.",
            "url": repo.html_url, "language": repo.language or "Not specified",
            "tech_stack": tech_stack, "stars": repo.stargazers_count,
            "forks": repo.forks_count, "topics": repo.get_topics(),
            "important_files": important_files
        }
    except GithubException as e:
        if e.status == 404: raise Exception("Repository not found. Please check the URL.")
        elif e.status == 401: raise Exception("Authentication error. Please check your GitHub token.")
        else: raise Exception(f"Error fetching repo data: {str(e)}")


# --- AI Agent & Workflow Functions ---
# *** THIS IS THE CORRECTED AND STABLE IMPLEMENTATION ***

async def run_ai_analysis(repo_data: dict, api_key: str):
    """
    Runs a single, robust AI analysis using the reliable summarize_text method
    to get a structured overview and key features.
    """
    from iointel import Agent, Workflow

    context = f"""
    Repository Name: {repo_data['name']}
    Description: {repo_data['description']}
    Primary Language: {repo_data['language']}
    Topics: {', '.join(repo_data['topics'])}
    
    Key File Contents:
    """
    for path, content in repo_data['important_files'].items():
        context += f"\n--- Start of {path} ---\n{content[:1500]}\n--- End of {path} ---\n"

    try:
        # We use one agent with very specific instructions for the tool it will use.
        analyst_agent = Agent(
            name="Expert Repo Analyst",
            instructions="""
            You are an expert GitHub repository analyst who will use the `summarize_text` tool.
            - For the 'summary' parameter, you MUST provide a detailed overview covering the project's purpose, main functionality, and target audience.
            - For the 'key_points' parameter, you MUST create a bulleted list of the top 3-5 technical features, the core technologies used, and the essential 'getting started' commands.
            """,
            model="meta-llama/Llama-3.3-70B-Instruct",
            api_key=api_key,
            base_url="https://api.intelligence.io.solutions/api/v1"
        )
        
        prompt = f"Please provide a comprehensive analysis of the following repository context:\n{context}"
        workflow = Workflow(objective=prompt, client_mode=False)
        
        # *** THE CRITICAL FIX IS HERE ***
        # We make ONE reliable call to summarize_text, which is designed to return a SummaryResult object.
        # This prevents the 'str' object has no attribute 'summary' error.
        results_object = (await workflow.summarize_text(max_words=600, agents=[analyst_agent]).run_tasks())["results"]["summarize_text"]
        
        # Now we can safely access the attributes of the returned object.
        return {
            "overview": results_object.summary,
            "features": results_object.key_points
        }

    except Exception as e:
        # This will now only catch genuine API errors, not type errors from our code.
        raise Exception(f"An error occurred with the AI analysis. Please check your IO Intelligence API key. Details: {str(e)}")


# --- Streamlit UI (No changes needed, but included for completeness) ---

def main():
    """Main function to run the Streamlit application."""
    st.title("🤖 AI GitHub Repo Analyst")
    st.markdown("Enter a public GitHub repository URL and your API keys to get a deep, AI-powered analysis.")

    with st.sidebar:
        st.header("⚙️ Configuration")
        st.markdown("Enter your API keys below. Your keys are not stored.")
        
        github_token = st.text_input(
            "GitHub Personal Access Token", type="password",
            help="Create a token with `public_repo` scope [here](https://github.com/settings/tokens)."
        )
        iointel_api_key = st.text_input(
            "IO Intelligence API Key", type="password",
            help="Get your key from the IO Intelligence dashboard."
        )
        st.info("This app uses a 'Bring Your Own Key' model. Your keys are used only for this session and are not saved.")

    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="e.g., https://github.com/microsoft/autogen",
        key="repo_url_input"
    )

    if st.button("Analyze Repository", type="primary"):
        if not github_token or not iointel_api_key:
            st.warning("Please enter both your GitHub Token and IO Intelligence API Key in the sidebar.")
            st.stop()
        if not repo_url:
            st.warning("Please enter a repository URL.")
            st.stop()
        
        try:
            repo_name = validate_repo_url(repo_url)
            g = Github(github_token)
            
            with st.status("Analyzing Repository...", expanded=True) as status:
                st.write(f"🔍 Fetching data for `{repo_name}`...")
                repo_data = fetch_repo_data(g, repo_name)
                st.session_state.repo_data = repo_data
                
                st.write("🧠 Performing AI analysis with IO Intelligence...")
                ai_results = asyncio.run(run_ai_analysis(repo_data, iointel_api_key))
                st.session_state.ai_results = ai_results
                
                status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

            st.session_state.analysis_complete = True

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.session_state.analysis_complete = False

    if st.session_state.get("analysis_complete", False):
        repo_data = st.session_state.repo_data
        ai_results = st.session_state.ai_results

        st.subheader(f"Analysis for: [{repo_data['owner']}/{repo_data['name']}]({repo_data['url']})")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("⭐ Stars", repo_data['stars'])
        col2.metric("🍴 Forks", repo_data['forks'])
        col3.metric("🗣️ Primary Language", repo_data['language'])
        
        st.markdown("**Description:**")
        st.info(repo_data['description'])
        
        st.markdown("**Detected Technology Stack & Topics:**")
        tech = repo_data['tech_stack'] + repo_data.get('topics', [])
        st.write(' '.join(f"`{t}`" for t in tech))

        st.subheader("📝 In-Depth AI Analysis")
        st.markdown(ai_results['overview'])

        st.markdown("#### Key Features & Technical Details")
        for point in ai_results['features']:
            st.markdown(f"- {point}")

if __name__ == "__main__":
    main()