import telegram
import openai
import os

# Authenticate with the Chat GPT API
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set up your Telegram bot with your token
bot = telegram.Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])

# Define a function to handle incoming messages
def handle_message(update, context):
    # Get the text of the incoming message
    message_text = update.message.text

    # Use the Chat GPT API to generate a response
    response = openai.Completion.create(
        engine="davinci",
        prompt=message_text,
        max_tokens=60
    )

    # Use the Telegram Bot API to send the response back to the user
    bot.send_message(chat_id=update.effective_chat.id, text=response.choices[0].text)

# Set up your webhook to receive incoming messages
updater = telegram.ext.Updater(token=os.environ["TELEGRAM_BOT_TOKEN"])
updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
updater.start_webhook(listen="0.0.0.0", port=int(os.environ.get("PORT", "8443")), url_path=os.environ["TELEGRAM_BOT_TOKEN"])
updater.bot.setWebhook("https://<your-app-name>.herokuapp.com/" + os.environ["TELEGRAM_BOT_TOKEN"])
updater.idle()
