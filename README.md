<p align="center">
  <img src="1.png" alt="AI Repo Analyst Logo" width="200">
</p>

<h1 align="center">🤖 AI GitHub Repo Analyst</h1>

<p align="center">
  <b>A Streamlit web application that uses AI to provide an in-depth analysis of any public GitHub repository.</b>
  <br><br>
  <a href="https://app-repo-analyst-appstxxiw3ley4gxx4ul9pa.streamlit.app/">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Streamlit App">
  </a>
</p>

---

## 📖 Overview

This project is a powerful tool for developers, project managers, and tech enthusiasts who want to quickly understand the purpose, structure, and key features of a GitHub repository without manually sifting through code.

By simply providing a repository URL and your API keys, the application fetches critical data, reads key files, and leverages the **IO Intelligence API** to generate a comprehensive and insightful analysis.

## ✨ Key Features

-   **Dynamic Repo Fetching**: Analyzes any public GitHub repository using its URL.
-   **Deep Contextual Analysis**: Reads the content of important files like `README.md`, `requirements.txt`, and `package.json` to provide a richer context to the AI.
-   **In-Depth AI Insights**: Generates a structured analysis that includes:
    -   A detailed overview of the project's purpose and target audience.
    -   A bulleted list of key technical features and capabilities.
    -   Inferred "getting started" commands for quick setup.
-   **"Bring Your Own Key" (BYOK) Model**: Securely uses your personal API keys for GitHub and IO Intelligence, which are entered in the sidebar and never stored.
-   **Tech Stack Detection**: Automatically identifies the primary languages and technologies used in the repository.

## 📸 Application Screenshot

*This is what the application looks like in action!*

<p align="center">
  <img src="https://github.com/user-attachments/assets/6ae5a28a-840e-4db8-a1eb-0b4965adf161" alt="Application Screenshot" width="800">
</p>

## 🛠️ How It Works & Tech Stack

The application follows a simple yet powerful architecture:

1.  **Frontend**: Built with **Streamlit** for a fast, interactive user interface.
2.  **GitHub API**: Uses the **PyGithub** library to fetch repository data, including metadata and file contents.
3.  **AI Backend**: Leverages the **IO Intelligence API** and a Llama 3.3 70B model to analyze the collected data and generate structured insights.

The core technologies are:
-   **Python**
-   **Streamlit**
-   **PyGithub**
-   **IO Intelligence**

## 🚀 Getting Started

There are two ways to use the application:

### 1. Access the Live Demo

The easiest way to get started is to use the deployed version on Streamlit Community Cloud:

**[➡️ Click here to launch the live application!](https://app-repo-analyst-appstxxiw3ley4gxx4ul9pa.streamlit.app/)**

### 2. Run Locally

If you want to run the application on your own machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
    The application will open in your browser.

## 🔑 Configuration

The application requires two API keys to function:

1.  **GitHub Personal Access Token**: Needed to interact with the GitHub API and avoid rate limits. You can generate one [here](https://github.com/settings/tokens) with `public_repo` scope.
2.  **IO Intelligence API Key**: Required for the AI analysis. You can get this from your IO Intelligence dashboard.

These keys are entered in the sidebar of the application and are used only for the current session. **They are never stored or saved.**

---

<p align="center">
  Made with ❤️ and Python. Congratulations on your project!
</p>
