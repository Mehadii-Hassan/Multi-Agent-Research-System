# Multi-Agent-Research-System

A Streamlit-powered research assistant that combines web search, web scraping, and generative AI to build structured reports and provide constructive critique.

## What this project does

- Uses a search agent to discover recent, relevant information.
- Uses a reader agent to scrape and summarize content from selected URLs.
- Uses a writer chain to produce a polished research report.
- Uses a critic chain to review the report and provide feedback.

## Setup

1. Create and activate the Conda environment:

```bash
conda create -n multiagent python=3.11 -y
conda activate multiagent
```

2. Install the project dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the repository root with your environment variables:

```env
GITHUB_TOKEN=your_github_token_here
TAVILY_API_KEY=your_tavily_api_key_here
```

> Note: `GITHUB_TOKEN` is used for the OpenAI-compatible model backend, and `TAVILY_API_KEY` is used for web search.

## Run the application

### Option 1: Start the Streamlit app

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal.

### Option 2: Run the research pipeline directly

```bash
python main.py
```

This will execute the research pipeline for a sample topic defined in `main.py`.

## Project structure

- `app.py` - Streamlit frontend and UI styling.
- `main.py` - Example pipeline runner for direct execution.
- `src/agents/agents.py` - Agent and chain configuration.
- `src/pipelines/pipeline.py` - Research workflow that orchestrates search, scraping, writing, and critique.
- `src/tools/tools.py` - Search and scraping tools used by the agents.
- `requirements.txt` - Python package dependencies.

## Notes

- The app uses `langchain`, `streamlit`, and `tavily`.
- If you encounter SSL certificate issues on Windows, make sure `certifi` is installed and that your Python environment can access system certificate bundles.
- Keep your `.env` file private and do not commit it to source control.

## License

This repository includes a `LICENSE` file. Please review it for the licensing terms.
