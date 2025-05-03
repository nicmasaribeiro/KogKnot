from flask import Flask, render_template,send_from_directory, request, redirect, abort, jsonify,sessions, Response, url_for,send_file,render_template_string,flash
from flask import Blueprint
from flask_caching import Cache
import asyncio
import socket
import os
import html
import os
import statsmodels.api as sm
from quart import Quart
from web3 import Web3
import os
import csv
import random
import subprocess as sp
import xml.etree.ElementTree as ET
import scipy
from flask_executor import Executor
import xml.dom.minidom
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, save
from bokeh.embed import file_html, components
from bokeh.resources import CDN
import matplotlib.pyplot as plt
import datetime as dt
import base64
import requests
from models import *
from sqlalchemy import create_engine
from cryptography.hazmat.primitives.asymmetric import rsa as _rsa
from cryptography.hazmat.primitives import serialization
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename
from sqlalchemy import delete
import json
import yfinance as yf
import stripe
from flask_login import current_user, login_required, login_user
import time
from hashlib import sha256
from subprocess import Popen, PIPE
import openai
import threading
from sklearn.linear_model import LinearRegression 
import fastapi
import socket
import websocket as ws
import asyncio
import threading
import plotly.express as px
import plotly
from scipy.integrate import quad
from scipy.stats import poisson
from sqlalchemy.orm import scoped_session, sessionmaker
import uuid
import logging
import schedule # apscheduler.schedulers.background import BackgroundScheduler
import threading
from flask import session
from arch import arch_model
from celery import Celery
import ssl
from flask_login import LoginManager
import redis
from sklearn.decomposition import PCA
import subprocess
from kaggle_ui import kaggle_bp
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from models import db  # wherever db is defined

migrate = Migrate(app, db)

	
stripe.api_key = 'sk_test_51OncNPGfeF8U30tWYUqTL51OKfcRGuQVSgu0SXoecbNiYEV70bb409fP1wrYE6QpabFvQvuUyBseQC8ZhcS17Lob003x8cr2BQ'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.config['SECRET_KEY'] = os.urandom(32).hex()  # Change to a strong secret
app.config['CACHE_TYPE'] = 'simple'  # Simple in-memory cache
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout (in seconds)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

cache = Cache(app)
executor = Executor(app)

DOWNLOAD_FOLDER = os.path.abspath("./local")  # or wherever your files are stored

app.register_blueprint(kaggle_bp, url_prefix="/app")
 

@login_manager.user_loader
def load_user(user_id):
    return Customers.query.get(int(user_id))

@app.route('/buy/cash', methods=['GET'])
@login_required
def buy_cash():
	return render_template('stripe-payment.html')


@app.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
	try:
		user_id = current_user.id  # Assuming you're using Flask-Login
		
		checkout_session = stripe.checkout.Session.create(
			payment_method_types=['card'],
			line_items=[{
				'price_data': {
					'currency': 'usd',
					'product_data': {
						'name': 'Purchase Cash',
					},
					'unit_amount': 5000,  # Amount in cents ($50.00)
				},
				'quantity': 1,
			}],
			mode='payment',
			success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
			cancel_url=url_for('cancel', _external=True),
			metadata={
				'user_id': user_id  # Store user_id in the metadata
			}
		)
		return redirect(checkout_session.url, code=303)
	except Exception as e:
		return jsonify(error=str(e)), 403
	
@app.route('/success')
def success():
	session_id = request.args.get('session_id')
	session = stripe.checkout.Session.retrieve(session_id)
	if session.payment_status == 'paid':
		user_id = session.metadata['user_id']  # Retrieve user_id from metadata
		user = Customers.query.get_or_404(user_id)
		user_balance = WalletDB.query.filter_by(address=user.username).first()
		user_balance.balance += 50  # Adding $50 to user's balance, modify as needed
		db.session.commit()
		pay_id =  session.payment_intent
		user.payment_id = pay_id
		db.session.commit()
		return f"<h1>Payment Successful</h1><a href='/'>Home</a><h3>{pay_id}</h3>"
	else:
		return '<h1>Payment Failed</h1><a href="/">Home</a>'
	
@app.route('/cancel')
def cancel():
	return '<h1>Payment Cancelled</h1><a href="/">Home</a>'

@app.route('/sell/cash', methods=['GET', 'POST'])
@login_required
def sell_cash():
	if request.method == 'POST':
		amount = request.form['amount']
		user_id = current_user.id  # Assuming you're using Flask-Login
		user = Customers.query.get(user_id)
		user_balance = WalletDB.query.filter_by(address=user.username).first()
		
		if user_balance.balance >= float(amount):
			# Deduct the balance from the user's wallet
			user_balance.balance -= float(amount)
			db.session.commit()
			
			# Create a refund in Stripe
			try:
				# You need to keep track of the payment intent ID during the payment process
				payment_intent_id = request.form['payment_intent_id']  # You'll need to pass this from the frontend
				refund = stripe.Refund.create(
					payment_intent=payment_intent_id,
					amount=int(float(amount) * 100),  # amount in cents
				)
				return jsonify({'message': 'Refund Successful', 'refund': refund}), 200
			except Exception as e:
				return jsonify(error=str(e)), 403
		else:
			return jsonify({'message': 'Insufficient Balance'}), 400
	return render_template('sell-cash.html')

@app.route('/')
def base():
	return render_template('index_base.html')

@app.route('/register', methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username = request.values.get("username")
        email = request.values.get("email")
        cell_number = request.values.get("cell_number")
        password = request.values.get("password")

        # Check for existing user
        existing_user = Customers.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # unique_address = os.urandom(10).hex()
        # new_user = Customers(
        #     username=username,
        #     email=email,
        #     cell_number=cell_number,
        #     password=hashed_password,
        #     personal_token=os.urandom(10).hex(),
        #     private_token=unique_address)

        # db.session.add(new_user)
        # db.session.commit()
        return jsonify({'message': 'User created!'}), 201

    return render_template("signup.html")


@app.route('/register/wallet', methods=['POST','GET'])
def create_wallet():
	if request.method =="POST":
		username = request.values.get("username")
		password = request.values.get("password")
		users = Customers.query.all()
		ls = [user.username for user in users]
		passwords = [user.username for user in users]
		if username in ls:
			if password in passwords:
				data = os.urandom(10).hex()
				new_wallet = WalletDB(address=username,token=username,password=password,coinbase_wallet=data)
				db.session.add(new_wallet)
				db.session.commit()
				return jsonify({'message': 'Wallet Created!'}), 201
	return render_template("signup-wallet.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == "POST":
		username = request.values.get("username")
		password = request.values.get("password")
		user = Users.query.filter_by(username=username).first()
		if user and bcrypt.check_password_hash(user.password, password):
			login_user(user, remember=True)  # <-- Ensure "remember=True" for session persistence
			return redirect('/')
		else:
			flash("Invalid username or password. Please try again.", "danger")
			return redirect('/login')
	return render_template("login.html")

@app.route('/get/users', methods=['GET'])
@login_required
def get_users():
	users = Customers.query.all()
	users_list = [{'id': user.id, 'username': user.username,'publicKey':str(user.personal_token)} for user in users]
	return jsonify(users_list)

@app.route('/usercred', methods=["GET","POST"])
def user_cred():
	if request.method == "POST":
		user = request.values.get("cred")
		password = request.values.get("password")
		return redirect(f'/users/{user}/{password}')
	return render_template('user-cred.html')
		
@app.route('/html/mywallet',methods=['GET'])
@login_required
def html_wallet():
	user = current_user
	wallet = WalletDB.query.filter_by(address=user.username).first()
	return render_template("wallet.html",wallet=wallet)


@app.route('/buy/coins',methods=['GET','POST'])
def buy_coins():
	if request.method =="POST":
		exchange = 100
		value = float(request.values.get('value'))
		id = request.values.get('id')
		username = request.values.get('username')
		password = request.values.get('password')
		house = BettingHouse.query.get_or_404(1)
		user = Customers.query.filter_by(username=username).first()
		wal = WalletDB.query.filter_by(address=username).first()
		if user and bcrypt.check_password_hash(user.password, password):
			coins = float(value*exchange)
			if coins <= house.coins:
				house.coins -= coins
				db.session.commit()
				wal.balance -= value
				db.session.commit()
				wal.coins += coins
				db.session.commit()
		return """<a href='/'><h1>Home</h1></a><h3>Success</h3>"""
	return render_template("buycash.html")

@app.route('/sell/coins',methods=['GET','POST'])
def sell_coins():
	if request.method =="POST":
		# exchange = coin.dollar_value
		value = float(request.values.get('value'))
		username = request.values.get('username')
		password = request.values.get('password')
		house = BettingHouse.query.get_or_404(1)
		user = Customers.query.filter_by(username=username).first()
		wal = WalletDB.query.filter_by(address=username).first()
		if user and bcrypt.check_password_hash(user.password, password):
			if wal.coins >= value:
				house.coins += .05*value
				db.session.commit()
				cash = float(value*exchange*.95)
				wal.balance += cash
				db.session.commit()
				wal.coins -= value
				db.session.commit()
		return f"""<a href='/'><h1>Home</h1></a><h3>Success</h3><p>You've successfully sold {value} coins.</p>"""
	return render_template("sell.html")

if __name__ == '__main__':
	with app.app_context():
		# db.create_all()
		PendingTransactionDatabase.genisis() 
		app.run(host="0.0.0.0",port=2000)