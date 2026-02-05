from telegram.corrections import apply_correction

async def handle_user_correction(update, context):
    field = context.user_data["field"]
    original = context.user_data["original"]
    corrected = update.message.text
    user_id = str(update.effective_user.id)

    apply_correction(field, original, corrected, user_id)

    await update.message.reply_text(
        "✅ Correction saved and will be learned."
    )
