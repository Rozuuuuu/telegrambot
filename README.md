# 🤖 AI-Powered Telegram Bot

A smart Telegram bot built with Python that responds to user messages with AI-generated replies using OpenAI's GPT. Deployed 24/7 on Render for free.

---

## ✨ Features

- **AI-powered conversations** – Natural language replies via OpenAI GPT
- **Professional command menu** – `/start`, `/help`, `/ai <question>`
- **In-place "Thinking…" indicator** – Clean UX with edited messages
- **Dual-mode deployment** – Polling for local dev, webhooks for production
- **Robust error handling** – Graceful recovery from API errors and rate limits
- **Fully asynchronous** – Handles multiple users simultaneously

## 🛠️ Tech Stack

| Layer        | Technology              |
|--------------|-------------------------|
| Language     | Python 3.10+            |
| Telegram SDK | `python-telegram-bot`   |
| AI Engine    | OpenAI API (GPT-3.5)    |
| Hosting      | Render (free tier)      |

## 🚀 Live Demo

👉 [Try the bot on Telegram](https://t.me/your_bot_username)

> Replace `your_bot_username` with your actual bot's username.

---

## 🔧 Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/telegram-ai-bot.git
cd telegram-ai-bot

# 2. Create & activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
copy .env.example .env       # Windows
# cp .env.example .env       # macOS / Linux
# Then open .env and add your real BOT_TOKEN and OPENAI_API_KEY

# 5. Run the bot
python bot.py
```

Open Telegram, find your bot, and send a message — it should respond with an AI-generated reply. 🎉

---

## ☁️ Deploying to Render (Free, 24/7)

1. Push your code to a **public GitHub repository** (make sure `.env` is in `.gitignore`).
2. Go to [render.com](https://render.com) → **New +** → **Web Service**.
3. Connect your GitHub repo and configure:

   | Setting           | Value                        |
   |-------------------|------------------------------|
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `python bot.py`              |
   | **Plan**          | Free                         |

4. Add **Environment Variables** on Render:

   | Variable              | Value                                      |
   |-----------------------|--------------------------------------------|
   | `BOT_TOKEN`           | Your Telegram bot token                    |
   | `OPENAI_API_KEY`      | Your OpenAI API key                        |
   | `DEPLOY_MODE`         | `webhook`                                  |
   | `RENDER_EXTERNAL_URL` | `https://your-service.onrender.com`        |

5. Click **Create Web Service**. Done! 🚀

---

## 🔗 API Integrations

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [OpenAI API](https://platform.openai.com/docs)

## 🧠 What I Learned

- Building and deploying production-ready bots with webhooks
- Securing API keys with environment variables
- Integrating third-party AI APIs (OpenAI)
- CI/CD via GitHub + Render auto-deploys
- Asynchronous Python programming with `asyncio`

---

## 📁 Project Structure

```
telegram-ai-bot/
├── bot.py              # Main bot application
├── requirements.txt    # Pinned dependencies
├── .env.example        # Example environment file (safe to commit)
├── .gitignore          # Prevents committing secrets
├── README.md           # This file
└── LICENSE             # MIT license
```

## 📝 License

MIT — free to use and modify.
