
import os
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# ==============================
# CONFIGURATION
# ==============================

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TIMEZONE = ZoneInfo("Africa/Porto-Novo")

# Sessions horaires du Bénin
SESSIONS = [9, 10, 17, 21]

# Durée d'une session : 20 minutes
SESSION_DURATION = 20

# Expiration des signaux
EXPIRATION_MINUTES = 3

# Nombre maximum de signaux par session
MAX_SIGNALS = 4


# ==============================
# LOGGING
# ==============================

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ==============================
# COMMANDE START
# ==============================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    message = (
        "🤖 TAOTRADING SIGNALS\n\n"
        "Bienvenue dans ton bot de signaux Forex.\n\n"
        "📌 Commandes disponibles :\n"
        "/signal - Demander un signal\n"
        "/status - État du bot\n"
        "/help - Aide\n\n"
        "⏰ Sessions : 09h, 10h, 17h et 21h\n"
        "⏳ Expiration : 3 minutes\n\n"
        "⚠️ Les signaux ne garantissent pas de gains."
    )

    await update.message.reply_text(message)


# ==============================
# COMMANDE HELP
# ==============================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "📊 TAOTRADING SIGNALS\n\n"
        "Utilise /signal pour demander un signal.\n"
        "Utilise /status pour voir l'état du bot.\n\n"
        "Les signaux réels seront activés "
        "après connexion aux données Forex."
    )


# ==============================
# COMMANDE SIGNAL
# ==============================

async def signal(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    now = datetime.now(TIMEZONE).strftime("%H:%M:%S")

    message = (
        "📡 TAOTRADING SIGNALS\n\n"
        f"🕒 Heure Bénin : {now}\n"
        "📊 Marché : Forex\n"
        "⏳ Expiration : 3 minutes\n\n"
        "⏸️ AUCUN SIGNAL CONFIRMÉ\n\n"
        "Le système attend les données du marché.\n\n"
        "⚠️ Ceci n'est pas un signal de trading réel."
    )

    await update.message.reply_text(message)


# ==============================
# COMMANDE STATUS
# ==============================

async def status(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    now = datetime.now(TIMEZONE)

    await update.message.reply_text(
        "🤖 TAOTRADING SIGNALS\n\n"
        "🟢 Bot actif\n"
        f"🕒 Heure Bénin : {now.strftime('%H:%M:%S')}\n"
        "📊 Marché : Forex\n"
        "⏳ Expiration : 3 minutes\n"
        "📡 Données Forex : Non connectées\n\n"
        "Le bot est prêt pour la prochaine étape."
    )


# ==============================
# MESSAGE AUTOMATIQUE
# ==============================

async def send_session_message(
    context: ContextTypes.DEFAULT_TYPE
):
    message = (
        "📡 TAOTRADING SIGNALS\n\n"
        "🔔 SESSION DE TRADING\n\n"
        "📊 Marché : Forex\n"
        "⏳ Durée : 20 minutes\n"
        "📈 Maximum : 4 signaux\n"
        "⌛ Expiration : 3 minutes\n\n"
        "⏸️ Aucun signal confirmé pour le moment.\n"
        "Les données Forex réelles ne sont pas encore connectées.\n\n"
        "⚠️ Pas de garantie de profit."
    )

    if CHAT_ID:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=message
        )

        logger.info("Message de session envoyé.")


# ==============================
# PLANIFICATION DES SESSIONS
# ==============================

def schedule_sessions(app: Application):

    for hour in SESSIONS:

        app.job_queue.run_daily(
            send_session_message,
            time=datetime.strptime(
                f"{hour:02d}:00",
                "%H:%M"
            ).time().replace(
                tzinfo=TIMEZONE
            ),
            name=f"session_{hour}",
        )

        logger.info(
            f"Session programmée à {hour:02d}:00"
        )


# ==============================
# FONCTION PRINCIPALE
# ==============================

def main():

    if not TOKEN:
        raise ValueError(
            "TELEGRAM_TOKEN n'est pas configuré."
        )

    app = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler("signal", signal)
    )

    app.add_handler(
        CommandHandler("status", status)
    )

    schedule_sessions(app)

    print("🤖 Taotrading Signals est en ligne !")
    print("⏰ Sessions : 09h, 10h, 17h et 21h")
    print("📡 En attente des données Forex...")

    app.run_polling()


# ==============================
# LANCEMENT
# ==============================

if __name__ == "__main__":
    main()
    
