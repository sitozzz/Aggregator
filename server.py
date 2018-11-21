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
import functions
import sdek_api
import dpd_api
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
   
    #=== Match tariffs ===
    sdek_id, pony_id, another_id = functions.match_tariffs(req, 'tariffs.csv', 'cp1251')
    #=== Match tariffs ===
    # Send requests to all API here
    # ==SDEK API==
    sdek_res = sdek_api.calculate_sdek(req, sdek_id)
    sdek_res = json.loads(sdek_res,encoding='utf-8')
    # ==SDEK API==
    
    #dpd_res = dpd_api.get_service_cost(req['city1']['name'],req['city2']['name'],True,True,int(req['goods']['weight']),int(req['goods']['length']),int(req['goods']['width']),int(req['goods']['height']))
    print(req['goods'][0]['weight'])
    print(type(req['goods'][0]['weight']))
    print(float(req['goods'][0]['weight']))
    print(type(req['goods'][0]['weight']))

    dpd_res = dpd_api.get_service_cost(req['city1']['name'].split(',')[0],req['city2']['name'].split(',')[0],True,True,req['goods'][0]['weight'],20,20,20)
    print(dpd_res['list'])
    # return results here

    out_json = jsonify({
        "sdek": sdek_res,
        "dpd": dpd_res['list'],
        "boxberry": "boxberry_json"
    })
    print(out_json)
   
    return out_json

    
@app.route('/get_tariffs', methods=['GET'])
def get_tariffs():
    # TODO: get tariffs from CSV file or database
    out_json = []
    with open('tariffs.csv', 'r', newline = '', encoding = 'cp1251') as file:
        reader = csv.DictReader(file, delimiter = ';')
        for i in reader:
            out_json.append(i['tariff_name'])
    print(out_json)
    return jsonify({
        'fields' : out_json
        })


if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=8000)
