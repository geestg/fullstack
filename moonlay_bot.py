import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

# =====================
# CONFIG
# =====================
BASE_URL = "http://127.0.0.1:8000"
TOKEN_FILE = "jwt_tokens.txt"  # file hasil get_jwt_tokens.py
USER_EMAIL = "admin@mail.com"  # user yang dipakai untuk bot

# =====================
# Load JWT token
# =====================
def load_token(email):
    try:
        with open(TOKEN_FILE, "r") as f:
            for line in f:
                if line.startswith(email):
                    return line.strip().split(": ")[1]
    except FileNotFoundError:
        print(f"[ERROR] {TOKEN_FILE} tidak ditemukan")
    return None

JWT_TOKEN = load_token(USER_EMAIL)
if not JWT_TOKEN:
    raise Exception("Tidak bisa melanjutkan, token JWT tidak tersedia!")

HEADERS = {"Authorization": f"Bearer {JWT_TOKEN}"}

# =====================
# Logging
# =====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# =====================
# COMMAND HANDLERS
# =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Moonlay Bot siap 🚀")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(f"{BASE_URL}/tasks", headers=HEADERS)
        response.raise_for_status()
        tasks = response.json()
        if not tasks:
            await update.message.reply_text("Belum ada task 😅")
            return
        msg = "Daftar Task:\n"
        for t in tasks:
            msg += f"{t['id']}. {t['title']} [{t['status']}] - Assignee: {t['assignee_id']}\n"
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# =====================
# MAIN
# =====================
if __name__ == "__main__":
    # Ambil token bot Telegram dari BotFather
    TELEGRAM_BOT_TOKEN = "<YOUR_TELEGRAM_BOT_TOKEN>"

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register command
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tasks", list_tasks))

    print("Moonlay Bot running...")
    app.run_polling()
