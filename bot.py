"""
AI-Powered Telegram Bot
========================
A smart Telegram bot that responds to user messages with AI-generated replies
using the OpenAI API. Supports both polling (development) and webhook (production) modes.

Author: Lloyd
License: MIT
"""

import os
import logging
from dotenv import load_dotenv
import openai
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Optional: override the default OpenAI model via an env var
AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")

# Deployment mode: "polling" for local dev, "webhook" for Render / production
DEPLOY_MODE = os.getenv("DEPLOY_MODE", "polling")

# Render provides this automatically when deployed
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "")

# Webhook port (Render injects PORT)
PORT = int(os.getenv("PORT", 8443))

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# OpenAI client
# ---------------------------------------------------------------------------
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# System prompt — tweak this to change the bot's personality
SYSTEM_PROMPT = (
    "You are a helpful, friendly AI assistant on Telegram. "
    "Keep your replies concise (under 300 words) and well-formatted. "
    "Use emojis sparingly to keep things readable."
)


# ---------------------------------------------------------------------------
# Command Handlers
# ---------------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when /start is issued."""
    welcome = (
        "🤖 *Hello! I'm your AI-powered assistant.*\n\n"
        "Just send me any message and I'll reply intelligently using AI.\n\n"
        "*Commands:*\n"
        "/start – Show this welcome message\n"
        "/help  – Get usage help\n"
        "/ai `<question>` – Ask the AI directly\n"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show a help message when /help is issued."""
    help_text = (
        "💡 *How to use this bot:*\n\n"
        "• Send me any text and I'll generate a smart AI reply.\n"
        "• Use /ai followed by your question for a direct query.\n"
        "• Example: `/ai What is the capital of France?`\n\n"
        "I'm powered by OpenAI — feel free to ask anything!"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /ai command — expects a question after the command."""
    # Grab everything after '/ai '
    query = " ".join(context.args) if context.args else ""
    if not query:
        await update.message.reply_text(
            "Please provide a question after /ai.\n"
            "Example: `/ai What is quantum computing?`",
            parse_mode="Markdown",
        )
        return
    await _generate_and_reply(update, query)


# ---------------------------------------------------------------------------
# Message Handler (catches all non-command text)
# ---------------------------------------------------------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Forward every plain-text message to the AI and reply."""
    user_message = update.message.text
    if not user_message:
        return
    await _generate_and_reply(update, user_message)


# ---------------------------------------------------------------------------
# Core AI Helper
# ---------------------------------------------------------------------------
async def _generate_and_reply(update: Update, user_message: str) -> None:
    """Call the OpenAI API and send the response back to the user."""
    # Show a "thinking" indicator so the user knows work is happening
    thinking_msg = await update.message.reply_text("🤔 Thinking...")

    try:
        response = openai_client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            max_tokens=1024,
            temperature=0.7,
        )
        ai_reply = response.choices[0].message.content

        # Edit the "Thinking..." message to show the actual reply
        await thinking_msg.edit_text(ai_reply)

    except openai.AuthenticationError:
        logger.error("OpenAI authentication failed — check your API key.")
        await thinking_msg.edit_text(
            "⚠️ AI service authentication failed. Please contact the bot admin."
        )
    except openai.RateLimitError:
        logger.warning("OpenAI rate limit hit.")
        await thinking_msg.edit_text(
            "⏳ The AI is a bit busy right now. Please try again in a moment."
        )
    except Exception as exc:
        logger.exception("Unexpected error calling OpenAI: %s", exc)
        await thinking_msg.edit_text(
            "❌ Something went wrong. Please try again later."
        )


# ---------------------------------------------------------------------------
# Error Handler
# ---------------------------------------------------------------------------
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error("Update '%s' caused error: %s", update, context.error)


# ---------------------------------------------------------------------------
# Post-Init: Set Bot Commands Menu
# ---------------------------------------------------------------------------
async def post_init(application: Application) -> None:
    """Set the bot's command menu in Telegram after startup."""
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Show available commands"),
        BotCommand("ai", "Ask the AI anything"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info("Bot commands menu set successfully.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    """Build and run the Telegram bot application."""

    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is not set!")
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set!")

    # Build the application
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ai", ai_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    # Start the bot in the appropriate mode
    if DEPLOY_MODE == "webhook" and RENDER_EXTERNAL_URL:
        webhook_url = f"{RENDER_EXTERNAL_URL}"
        logger.info("Starting bot in WEBHOOK mode → %s", webhook_url)
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=webhook_url,
        )
    else:
        logger.info("Starting bot in POLLING mode (local development).")
        app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
