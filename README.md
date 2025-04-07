# AI Smart Assistant 🤖📧

An intelligent, AI-powered personal email assistant that summarizes Gmail messages, sends updates via Slack, and integrates with Google Calendar. Built with Streamlit and powered by Cohere's language model.

---

## 🚀 Features

- 📥 **Gmail Integration**: Authenticates and fetches emails using Gmail API.
- 🧠 **LLM-based Summarization**: Uses Cohere API to summarize email content.
- 🔔 **Slack Integration**: Sends daily digest and email summaries to your Slack via a bot.
- 📆 **Calendar Summary**: Integrates with Google Calendar to summarize events.
- 🖥️ **Streamlit Dashboard**: View summaries directly in the browser.
- 🧪 **Test Scripts**: Validate email parsing, summarization, and Slack posting.

---

## 📁 Project Structure

```bash
AI-Smart-Assistant/
│
├── authenticate_google.py        # Handles Gmail and Calendar OAuth
├── calendar_summary_service.py   # Summarizes Google Calendar events
├── credentials.json              # OAuth credentials (excluded from repo)
├── database.py                   # Email storage and lookup
├── email_dashboard.py            # Streamlit UI app
├── email_service.py              # Fetches Gmail messages
├── email_summary_service.py      # Summarizes emails via Cohere
├── email_to_slack.py             # Sends summary to Slack
├── llm_service.py                # Cohere LLM service wrapper
├── slack_service.py              # Posts messages to Slack
├── slack_notifier.py             # Slack message formatter
├── get_user_id.py                # Helper for Slack user ID
├── token.json                    # OAuth tokens (excluded from repo)
├── test_email_summary.py         # Unit test for summarization
├── test_slack.py                 # Slack test script
├── README.md                     # You are here
├── .env                          # Environment variables (excluded)
└── .gitignore                    # Ensures secrets aren’t committed
