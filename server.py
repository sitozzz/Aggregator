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
    print('Request: ')
    print(req)
    # Match city names
    # Send requests to all API here
    # ==SDEK API==
    # TODO: send request to sdek
    sdek_json = {
        "version":"1.0",
        "dateExecute": req['dateExecute'], 
        # "authLogin":"098f6bcd4621d373cade4e832627b4f6", 
        # "secure":"396fe8e7dfd37c7c9f361bba60db0874", 
        "senderCityId": req['city1']['id'], 
        "receiverCityId": req['city2']['id'], 
        # Check this
        "tariffId":"11", 
        "goods": req['goods'],
        # "services": [
        #     {	
        #         "id": 2,	
        #         "param": 2000	
        #     },
        #     {	
        #         "id": 30
        #     }
        # ]
    }
    
    sdek_res = requests.post('http://api.cdek.ru/calculator/calculate_price_by_json.php',json=sdek_json)
    sdek_res = sdek_res.text
    # sdek_res = json.loads(sdek_res)
    # ==SDEK API==
    
    # return results here
    return jsonify(sdek_res)
    # TODO: send this!
    # return jsonify({
    #     'company_name': 321,
    #     'company_name1': 21,
    #     'company_name3': 184
    # })

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=8000)
