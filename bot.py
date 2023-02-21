from telegram.ext import Updater, CommandHandler
import requests
import json
import os

TOKEN = "YOUR_TOKEN_HERE"

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm a bot that can search for post links. Just send me the keyword you want to search for.")

def search(update, context):
    query = ' '.join(context.args)
    url = f"https://api.telegram.org/bot{TOKEN}/search_post_links?query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()['result']
        if results:
            with open("links.txt", "w") as f:
                for result in results:
                    f.write(result['url'] + "\n")
            context.bot.send_message(chat_id=update.effective_chat.id, text="Here are the links I found:")
            context.bot.send_document(chat_id=update.effective_chat.id, document=open("links.txt", "rb"))
            os.remove("links.txt")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="No results found.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, something went wrong.")

if __name__ == '__main__':
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    search_handler = CommandHandler('search', search)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(search_handler)

    updater.start_polling()
