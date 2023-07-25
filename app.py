from flask import Flask, request, jsonify, flash
import json
import config
from binance.client import Client
from binance.enums import *
import telebot

app = Flask(__name__)
app.secret_key = b'123123123'
client = Client(config.api_key, config.secret_key)


def new_order(symbol, side, quantity, order_type=ORDER_TYPE_MARKET):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price='0.00001')

        telebot.TeleBot(config.telegram_api).send_message(
            config.telegram_user_id, f'{symbol}{side}{order_type}{quantity}')

        return order

    except Exception as e:
        print(str(e))

        return f'{str(e)}'


@app.route('/')
def index():
    return 'OK'


@app.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads(request.data)

    if data['passphrase'] != config.PASSPHRASE:
        return {
            'code': 'fail',
            'message': 'nice try'
        }

    # retrieve data from json and pass to new_order function
    symbol = ''
    side = ''
    quantity = ''
    order_type = ''
    order_response = new_order(symbol, side, quantity, order_type)

    if order_response:
        return {
            'code': 'success',
            'message': 'order executed',
        }
    else:
        return {
            'code': 'fail',
            'message': 'order failed',
            'response': order_response,
        }


if __name__ == '__main__':

    app.run(debug=True)
