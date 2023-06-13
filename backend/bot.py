from urllib import response
from cairo import Filter
from telegram import Update
import torch
from telegram.ext import MessageHandler, CallbackContext, CommandHandler, filters, Application
import json
import os

TOKEN = ""

class BankBot():
    def __init__(self):
        self.application = Application.builder().token(TOKEN).build()
        self.application.add_handler(CommandHandler('shop', self.addShop))
        self.application.add_handler(MessageHandler(filters.ALL, self.response))

        if os.path.isfile('./client.json'):
            with open("client.json") as fp:
                self.clients = json.load(fp)
        else:
            self.clients = {}

    def start_polling(self):
        print("start...")
        self.application.run_polling()
        
    async def response(self, update, context):
        q = update.message.text
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="我看不懂這個 {} 指令".format(q)
        )

    async def addShop(self, update, context):
        args = context.args
        if len(args) != 1:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="usage: /shop [YOUR_ADDRESS]"    
            )
        else:
            address = args[0]
            this.client[address] = update.effective_chat.id
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="已經設定 {} 的店家收款通知！"
            )
