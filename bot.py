import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from agent import ask_agent
from rag import ingest_pdf, search_pdf
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "8722568536:AAFX70oReJidH2qeLz7y26rMskViV58t2N0" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I'm your local AI assistant powered by Qwen 2.5.\n\n"
        "📄 Send me a PDF and I'll index it.\n"
        "💬 Then ask me anything about its contents!"
    )

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc.file_name.endswith(".pdf"):
        await update.message.reply_text("Please send a .pdf file.")
        return

    await update.message.reply_text(f"Received {doc.file_name}, processing...")
    file = await context.bot.get_file(doc.file_id)
    save_path = f"./uploads/{doc.file_name}"
    os.makedirs("./uploads", exist_ok=True)
    await file.download_to_drive(save_path)
    ingest_pdf(save_path, doc.file_name)
    await update.message.reply_text(f"✅ Indexed! Now ask me anything about {doc.file_name}")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.reply_text("🔍 Searching...")

    context_text = search_pdf(user_msg)
    augmented_prompt = f"""Use the following context from uploaded PDFs to answer the question.
If the answer isn't in the context, say so clearly.

Context:
{context_text}

Question: {user_msg}"""

    response = ask_agent(augmented_prompt)
    await update.message.reply_text(response)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()