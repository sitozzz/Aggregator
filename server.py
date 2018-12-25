# coding: utf-8
from flask import Flask, render_template, request, Response, redirect, url_for, flash, jsonify, send_file
from functools import wraps
from random import randint
import numpy as np
import json
import hashlib
import os
import shutil
import math
import random
import time
import requests
import pandas as pd
import csv
# import functions
import sdek_api
import dpd_api
import pony_api
import boxberry_api

app = Flask(__name__)

def check_auth(username, password):
    return username == 'user' and password == '123456'


def authenticate():
    return Response('Auth Failed', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/')
@app.route('/index', methods=['GET'])
# @requires_auth
def index():
    return render_template("index.html")

@app.route('/calculate', methods=['POST'])
def calculate():
    # Recieving request from user
    req = request.get_json()
    # print('Request: ')
    print(req)

    #TODO: Match city names
   
    # ==SDEK API==
    # TODO: Add from and to delivery selection
    sdek_res = sdek_api.calculate_sdek(req)
    # sdek_res = json.loads(sdek_res,encoding='utf-8')
    # ==SDEK API==
    
    dpd_res = dpd_api.get_service_cost(req)
    print(dpd_res['list'])

    #загрузить файлы
    #boxberry_api.data_loading()
    boxberry_res = boxberry_api.get_data_boxberry(req)
    
    # return results here

    pony_res = pony_api.get_service_cost(req)

    out_json = jsonify({
        "sdek": sdek_res,
        "dpd": dpd_res['list'],
        "boxberry": boxberry_res,
        "pony": pony_res
    })
    print(out_json)

    
   
    return out_json


@app.route('/sdek_pvz', methods=['POST'])
def sdek_pvz():
    req = request.get_json()
    output = sdek_api.get_pvz_list(req['city_code'])
    
    return jsonify(output)

@app.route('/sdek_delivery', methods=['POST'])
def sdek_delivery():
    req = request.get_json()
    out = sdek_api.add_delivery(req['date'], req['sender'], req['reciever'], req['package'])
    print(out)
    return jsonify({"Some data": "from sdek api"})


if __name__ == '__main__':
    
    app.run(host='127.0.0.1', port=8000, debug=True)
