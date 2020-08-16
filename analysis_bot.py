#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import saapi
import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('this is a whatsapp analysis bot\n 1) export cahat without media from any whatsapp group/convo and send .txt file here - only .txt not .vcf ')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    if update.message.document:
        token = "" #enter your bot token from bot father
        bot = telegram.Bot(token=token)
        file_id = update.message.document.file_id
        newfile = bot.get_file(file_id=file_id)
        update.message.reply_text("wait till we  process" ) 
        saapi.analysis((newfile.download()), update.message.chat_id ) #main
        update.message.reply_text("Made by - Ronak patil  follow me on insta @ronak.ig - https://www.instagram.com/ronak.ig/?hl=en")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("enter yout bot token", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.document, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
