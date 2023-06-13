'''
    python-telegram-bot: 13.7, version 20.XX cannot work
'''

from urllib import response
from cairo import Filter
from telegram import Update
import torch
from telegram.ext import MessageHandler, CallbackContext, CommandHandler, Filters, Updater
import json
import os

TOKEN = ""

class BankBot():
    def __init__(self):
        self.updater = Updater(TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler('start',   self.start))
        self.dispatcher.add_handler(CommandHandler('add',   self.add))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.echo))
        self.clients = {}

        if os.path.isfile('./client.json'):
            with open("client.json") as fp:
                self.clients = json.load(fp)
        else:
            self.clients = {}

    def start_polling(self):
        self.updater.start_polling()

    def echo(self, update, context):
        message = update.message.text
        context.bot.send_message(chat_id=update.effective_chat.id, text="我看不懂 {} 指令".format(message))

    def add(self, update, context):
        args = context.args

        if len(args) != 1:
            context.bot.send_message(chat_id=update.effective_chat.id, text="usage: /start YOUR_ADDRESS")
        else:
            address = args[0]
            self.clients[address] = update.effective_chat.id
            with open('client.json', 'w') as fp:
                json.dump(self.clients, fp)
            context.bot.send_message(chat_id=update.effective_chat.id, text="開始追蹤 {} 的出入帳通知".format(address))

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, 這是暨大區塊鏈銀行 Telegram Bot\n\n/add YOUR_ADDRESS: 追蹤出入帳通知")