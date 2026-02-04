# app/main.py

import os
import logging
import asyncio
from pathlib import Path

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes
)

from core.orchestrator import AccountingOrchestrator


# -----------------------------------------
# CONFIG
# -----------------------------------------

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TOKEN_HERE")
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)


# -----------------------------------------
# OPTIONAL INJECTION POINTS
# -----------------------------------------

async def dummy_cloud_ocr(images):
    return "", 0


async def dummy_llm(prompt):
    return "{}"


orchestrator = AccountingOrchestrator(
    cloud_ocr=None,   # plug provider later
    llm_callable=None # plug OpenAI later
)


# -----------------------------------------
# FILE DOWNLOAD
# -----------------------------------------

async def download_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    file = None

    if update.message.photo:
        file = await update.message.photo[-1].get_file()
        ext = ".jpg"

    elif update.message.document:
        file = await update.message.document.get_file()
        ext = Path(update.message.document.file_name).suffix

    else:
        await update.message.reply_text("Unsupported file type.")
        return None

    local_path = DOWNLOAD_DIR / f"{file.file_unique_id}{ext}"

    await file.download_to_drive(local_path)

    return str(local_path)


# -----------------------------------------
# MAIN MESSAGE HANDLER
# -----------------------------------------

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        await update.message.reply_text("📥 Document received")
        await update.message.reply_text("🔎 Running OCR...")

        file_path = await download_file(update, context)

        if not file_path:
            return

        await update.message.reply_text("🧠 Classifying & extracting accounting data...")

        result = await orchestrator.process_file(file_path)

        # ---------------------------------
        # Send Results Summary
        # ---------------------------------

        classification = result["document_classification"]
        confidence = result["confidence_metrics"]
        validation = result["validation_results"]

        summary_text = (
            f"📄 Type: {classification['document_type']}\n"
            f"🎯 Confidence: {confidence['overall']}%\n"
            f"✔ Validation: {validation['status']}"
        )

        await update.message.reply_text(summary_text)

        # ---------------------------------
        # Send Risk Warnings
        # ---------------------------------

        risks = result["risk_analysis"]["risks"]

        if risks:
            await update.message.reply_text(
                "⚠ Risks detected:\n" + "\n".join(risks)
            )

        # ---------------------------------
        # Send Export Files
        # ---------------------------------

        exports = result["export_files"]

        await update.message.reply_text("📤 Exporting accounting files...")

        if exports.get("excel"):
            await update.message.reply_document(
                open(exports["excel"], "rb")
            )

        if exports.get("xml"):
            await update.message.reply_document(
                open(exports["xml"], "rb")
            )

        if exports.get("csv"):
            for csv_file in exports["csv"]:
                await update.message.reply_document(open(csv_file, "rb"))

        await update.message.reply_text("✅ Processing completed")

    except Exception as e:

        logger.excepti

