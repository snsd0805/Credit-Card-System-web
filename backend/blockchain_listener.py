from web3 import Web3
from bot import BankBot

SBT_ADDRESS = ''
ABI = [
        {
          "anonymous": False,
          "inputs": [
            {
              "indexed": True,
              "internalType": "address",
              "name": "client",
              "type": "address"
            },
            {
              "indexed": True,
              "internalType": "address",
              "name": "bank",
              "type": "address"
            },
            {
              "indexed": False,
              "internalType": "uint256",
              "name": "id",
              "type": "uint256"
            },
            {
              "indexed": False,
              "internalType": "uint256",
              "name": "amount",
              "type": "uint256"
            }
          ],
          "name": "Repay",
          "type": "event"
        },
        {
          "anonymous": False,
          "inputs": [
            {
              "indexed": True,
              "internalType": "address",
              "name": "client",
              "type": "address"
            },
            {
              "indexed": True,
              "internalType": "address",
              "name": "shop",
              "type": "address"
            },
            {
              "indexed": True,
              "internalType": "address",
              "name": "bank",
              "type": "address"
            },
            {
              "indexed": False,
              "internalType": "uint256",
              "name": "id",
              "type": "uint256"
            },
            {
              "indexed": False,
              "internalType": "uint256",
              "name": "amount",
              "type": "uint256"
            }
          ],
          "name": "Borrow",
          "type": "event"
        }
    ]

class Listener():
    def __init__(self, bot: BankBot) -> None:
        self.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        self.contract = self.w3.eth.contract(address=SBT_ADDRESS, abi=ABI)
        self.bot = bot

    def handle_repay_event(self, event):
        print("Repay Event received:")
        print(event['args'])
        print("---")

        args = event['args']
        if args['client'] in self.bot.clients:
            chat_id = self.bot.clients[args['client']]
            self.bot.updater.bot.send_message(chat_id=chat_id, text="已經收到您編號 #{} 的帳款，共 {} ETH.".format(
                args['id'], int(args['amount'])/(10**18)
            ))

    def handle_borrow_event(self, event):
        print("Borrow Event received:")
        print(event['args'])
        print("---")

        args = event['args']
        if args['client'] in self.bot.clients:
            chat_id = self.bot.clients[args['client']]
            self.bot.updater.bot.send_message(chat_id=chat_id, text="您已經透過本銀行向 {} 支付 {} ETH. 帳款編號(#{})".format(
                args['shop'], int(args['amount'])/(10**18), args['id']
            ))
        
        if args['shop'] in self.bot.clients:
            chat_id = self.bot.clients[args['shop']]
            self.bot.updater.bot.send_message(chat_id=chat_id, text="本銀行已經先替客戶 {} 向您支付 {} ETH. 帳款編號(#{})".format(
                args['client'], int(args['amount'])/(10**18), args['id']
            ))

    def start(self):
        borrow_event_filter = self.contract.events.Borrow.create_filter(fromBlock='latest')
        repay_event_filter = self.contract.events.Repay.create_filter(fromBlock='latest')
        while True:
            for event in borrow_event_filter.get_new_entries():
                self.handle_borrow_event(event)
            for event in repay_event_filter.get_new_entries():
                self.handle_repay_event(event)