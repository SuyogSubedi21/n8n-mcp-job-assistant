# n8n + MCP Job Application Tracker

An AI-powered job hunt assistant built with n8n and a custom Python MCP server.

## What it does

• **CV Fit Checker:** upload your CV (PDF) and paste a job description into a form. An AI agent extracts the required skills, calls the MCP server's `check_cv_fit` tool, and returns a fit score with missing skills.

• **Gmail Job Tracker:** checks Gmail every hour. An AI agent classifies each email as a confirmation, interview, rejection, offer or not job-related, then updates a Postgres database through MCP tools. Job alerts and newsletters are ignored.

## Tech stack

• n8n (workflow automation, AI Agent node)
• Python MCP server (FastMCP, streamable HTTP)
• PostgreSQL (Docker)
• OpenRouter (gpt-4o-mini)
• Gmail API (OAuth)

## MCP tools

• `add_application`: save a new application with a status
• `update_status`: update an application's status by company name
• `get_stats`: count applications by status
• `check_cv_fit`: score a CV against required skills and years of experience (70% skills, 30% experience)

## Setup

1. Start Postgres:
   docker run -d --name jobs-postgres -e POSTGRES_USER=suyog -e POSTGRES_PASSWORD=yourpassword -e POSTGRES_DB=jobs -p 5432:5432 postgres

2. Create a `.env` file:
   DATABASE_URL=postgresql://suyog:yourpassword@localhost:5432/jobs

3. Run the MCP server:
   uv sync
   uv run server.py

4. Start n8n:
   docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n

5. Import the workflow JSON into n8n, then add your OpenRouter and Gmail credentials. Point the MCP Client Tool to http://host.docker.internal:8000/mcp.

## Author

Suyog Subedi · [GitHub](https://github.com/SuyogSubedi21)