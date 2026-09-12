
import os
import logging
from datetime import datetime

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "🤖 TAOTRADING SIGNALS\n\n"
        "Bienvenue dans ton bot de signaux Forex.\n\n"
        "Commandes disponibles :\n"
        "/signal - Demander un signal\n"
        "/help - Aide\n\n"
        "⚠️ Les signaux ne garantissent pas de gains."
    )
    await update.message.reply_text(message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 TAOTRADING SIGNALS\n\n"
        "Utilise /signal pour demander un signal.\n"
        "Les données Forex en direct seront ajoutées "
        "dans la prochaine étape."
    )


async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now().strftime("%H:%M")

    message = (
        "📡 TAOTRADING SIGNALS\n\n"
        f"🕒 Heure : {now}\n"
        "📊 Marché : Forex\n"
        "⏳ Expiration : 3 minutes\n\n"
        "⏸️ Aucun signal confirmé pour le moment.\n"
        "Le système attend les données du marché.\n\n"
        "⚠️ Pas de garantie de profit."
    )

    await update.message.reply_text(message)


def main():
    if not TOKEN:
        raise ValueError(
            "TELEGRAM_TOKEN n'est pas configuré."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("signal", signal))

    print("🤖 Taotrading Signals est en ligne !")
    app.run_polling()


if __name__ == "__main__":
    main()
  
