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
from flask import Blueprint, render_template, request, redirect, url_for, send_file,send_from_directory,jsonify
from werkzeug.utils import secure_filename
from models import NotebookSubmission, db
import nbformat
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from flask_login import login_required, current_user
from nbformat.v4 import new_notebook, new_code_cell
import io
import contextlib
import requests
import time
from models import UserNotebook
from flask import abort
import markdown
# from flask import Markup
import json
from markupsafe import Markup  # Instead of from flask import Markup
import markdown
from nbformat import reads as nbformat_reads
from nbformat import NO_CONVERT
from nbconvert.preprocessors import ExecutePreprocessor
import base64
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from io import BytesIO
from flask import current_app
from markupsafe import Markup
import markdown


proxy_list = [
"http://24.249.199.12:4145",
"http://45.77.67.203:8080",
"http://138.68.60.8:3128"
"http://50.174.7.157:80",
"http://172.66.43.12:80",
"http://133.18.234.13:80",
"http://81.169.213.169:8888",
"http://194.158.203.14:80"
]
	

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.config['SECRET_KEY'] = os.urandom(32).hex()  # Change to a strong secret
app.config['CACHE_TYPE'] = 'simple'  # Simple in-memory cache
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout (in seconds)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.StrictRedis(host='redis-server', port=6379)

cache = Cache(app)
executor = Executor(app)

DOWNLOAD_FOLDER = os.path.abspath("./local")  # or wherever your files are stored

openai.api_key = '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'
stripe.api_key = 'sk_test_51OncNPGfeF8U30tWYUqTL51OKfcRGuQVSgu0SXoecbNiYEV70bb409fP1wrYE6QpabFvQvuUyBseQC8ZhcS17Lob003x8cr2BQ'

app.config['CELERY_BROKER_URL'] = 'redis://red-cv8uqftumphs738vdlb0:6379'
app.config['CELERY_RESULT_BACKEND'] = 'redis://red-cv8uqftumphs738vdlb0:6379' 

app.register_blueprint(kaggle_bp, url_prefix="/app")
 
# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(result_backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.beat_schedule = {
    'run-every-minute': {
        'task': 'tasks.my_periodic_task',
        'schedule': 60.0,  # Run every 60 seconds
    },
}


@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

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
		user = Users.query.get_or_404(user_id)
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
		user = Users.query.get(user_id)
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

@app.route('/index')
def base():
	return render_template('index_base.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
	if request.method =="POST":
		password = request.values.get("password")
		username = request.values.get("username")
		email = request.values.get("email")
		cell_number = request.values.get("cell_number")
		unique_address = os.urandom(10).hex()
		hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
		new_user = Users(username=username, email=email,cell_number=cell_number, 
				   password=hashed_password,
				   personal_token=os.urandom(10).hex(),
				   private_token=unique_address)
		db.session.add(new_user)
		db.session.commit()
		return jsonify({'message': 'User created!'}), 201
	return render_template("signup.html")

@app.route('/signup/wallet', methods=['POST','GET'])
def create_wallet():
	if request.method =="POST":
		username = request.values.get("username")
		password = request.values.get("password")
		users = Users.query.all()
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
	users = Users.query.all()
	users_list = [{'id': user.id, 'username': user.username,'publicKey':str(user.personal_token)} for user in users]
	return jsonify(users_list)

@app.route('/signup/val', methods=['POST','GET'])
def signup_val():
	if request.method =="POST":
		password = request.values.get("password")
		username = request.values.get("username")
		users = Users.query.all()
		ls = [user.username for user in users]
		if username in ls:
			email = request.values.get("email")
			pk = str(os.urandom(10).hex())
			hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
			new_val = Peer(user_address=username, email=email, password=hashed_password,pk=pk)
			db.session.add(new_val)
			db.session.commit()
			return jsonify({'message': 'Val created!'}), 201
		else:
			pass
	return render_template("signup-val.html")


@app.route('/get/vals')
def get_vals():
	peers = Peer.query.all()
	peers_list = [{'id': peer.id, 'username': peer.user_address,'public_key':str(peer.pk)} for peer in peers]
	return jsonify(peers_list) #render_template('validators.html', vals=validators)

@app.route('/peer/<address>/<password>', methods=['GET'])
def get_peer(address,password):
	user = Peer.query.filter_by(user_address=address).first()
	if user and bcrypt.check_password_hash(user.password, password):
		return jsonify({'id': user.id,'coins':user.miner_wallet,'cash':user.cash})
	else:
		return "Wrong Password"

@app.route('/usercred', methods=["GET","POST"])
def user_cred():
	if request.method == "POST":
		user = request.values.get("cred")
		password = request.values.get("password")
		return redirect(f'/users/{user}/{password}')
	return render_template('user-cred.html')

@app.route('/valcred', methods=["GET","POST"])
def val_cred():
	if request.method == "POST":
		user = request.values.get("username")
		password = request.values.get("password")
		peer = Peer.query.filter_by(user_address=user).first()
		ls = {'id':peer.id,'user_address':peer.user_address,'coins':peer.miner_wallet,'cash':peer.cash}
		return jsonify(ls) 
	return render_template('val-cred.html')

@app.route('/my/transactions',methods=['GET','POST'])
def my_trans():
	if request.method == "POST":
		username = request.values.get('username')
		trans = TransactionDatabase.query.filter_by(username=username).all()
		ls = [{'name':t.username,'amount':t.amount,'type':str(t.type),'from_address':t.from_address,'to_address':t.to_address,'txid':t.txid} for t in trans]
		return jsonify(ls)
	return render_template("mytans.html")

@app.route('/html/my/transactions',methods=['GET','POST'])
def my_html_trans():
	if request.method == "POST":
		username = request.values.get('username')
		trans = TransactionDatabase.query.filter_by(username=username).all()
		return render_template("view_trans.html",trans=trans)
	return render_template("mytans.html")
		
@app.route('/users/<user>/<password>', methods=['GET'])
def get_user(user,password):
	user = Users.query.filter_by(username=user).first()
	if user and bcrypt.check_password_hash(user.password, password):
		return jsonify({'id': user.id, 'username': user.username,
				   'email': user.email,
				   'private_key':str(user.private_token),
				   'personal_token':str(user.personal_token),
				   'payment_id':user.payment_id})
	else:
		return redirect('/')

@app.route('/transact',methods=['GET','POST'])
def create_transact():
	if request.method == "POST":
		id_from = request.values.get("username_from")
		id_to = request.values.get("username_to")
		value = .9*float(request.values.get("value"))
		stake = coin.process_coins()
		password = request.values.get("password")
		user = Users.query.filter_by(username=id_from).first()
		user2 = Users.query.filter_by(username=id_to).first()
		w1 = WalletDB.query.filter_by(address=id_from).first()
		w2 = WalletDB.query.filter_by(address=id_to).first()
		packet = str({'from':id_from,'to':id_to,'value':value}).encode()
		blockchain.add_transaction(packet.hex())
		pending = PendingTransactionDatabase(
									   txid=os.urandom(10).hex(),
									   username=id_from,
									   from_address=w1.address,
									   to_address=id_to,
									   amount=value,
									   timestamp=dt.datetime.now(),
									   type='internal_wallet',
									   signature=str(w1.address).encode().hex())
		db.session.add(pending)
		db.session.commit()
		from_addrs = user.username
		to_addrs = user2.username
		txid = str(os.urandom(10).hex())
		transaction = {
				 'index': len(blockchain.pending_transactions)+1,
				 'previous_hash': sha512(str(blockchain.get_latest_block()).encode()).hexdigest(),
				 'timestamp':dt.date.today(),
				 'transactions': blockchain.pending_transactions,
				 'hash':sha256(str(blockchain.pending_transactions).encode())}
		blockchain.receipts['to'] = user2.username
		blockchain.receipts['from'] = user.username
		blockchain.receipts['value'] = value
		blockchain.receipts['txid'] = txid
		network.add_transaction(blockchain.pending_transactions)
		blockchain.add_transaction(transaction)
		blockchain.money.append(value)
		if user and bcrypt.check_password_hash(user.password, password):
			betting_house = BettingHouse.query.get_or_404(1)
			betting_house.cash_fee(.1*value)			
			new_value = 0.9*value
			w1.set_transaction(w2, new_value)
			new_transaction = TransactionDatabase(
										 username=user.username,
										 txid=txid,
										 from_address = from_addrs,
										 signature=os.urandom(10).hex(),
										 to_address = to_addrs,
										 amount = value, 
										 type='send')
			db.session.add(new_transaction)
			db.session.commit()
			coin_db = CoinDB.query.get_or_404(1)
			coin_db.gas(blockchain,6)
			return  """<a href='/'><h1>Home</h1></a><h3>Success</h3>"""
	return render_template("trans.html")

@app.route('/html/mywallet',methods=['GET'])
@login_required
def html_wallet():
	user = current_user
	wallet = WalletDB.query.filter_by(address=user.username).first()
	return render_template("wallet.html",wallet=wallet)


@app.route('/profile')
@login_required
def profile():
	user = current_user
	notifications = Notification.query.filter_by(receiver_id=user.username).order_by(Notification.timestamp.desc()).all()
	wallet = WalletDB.query.filter_by(address=user.username).first()
	portfolio = Portfolio.query.filter_by(username=user.username).all()
	investments = InvestmentDatabase.query.filter_by(owner=user.username).all()
	return render_template("nmbc_profile.html",user=user.username.upper(),notifications=notifications,wallet=wallet,portfolio=portfolio,investments=investments)

@app.route('/buy/coins',methods=['GET','POST'])
def buy_coins():
	if request.method =="POST":
		exchange = 100
		value = float(request.values.get('value'))
		id = request.values.get('id')
		username = request.values.get('username')
		password = request.values.get('password')
		house = BettingHouse.query.get_or_404(1)
		user = Users.query.filter_by(username=username).first()
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
		exchange = coin.dollar_value
		value = float(request.values.get('value'))
		username = request.values.get('username')
		password = request.values.get('password')
		house = BettingHouse.query.get_or_404(1)
		user = Users.query.filter_by(username=username).first()
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


UPLOAD_FOLDER = "./submissions"
ALLOWED_EXTENSIONS = {"ipynb"}
NOTEBOOK_FOLDER = "./submissions"

# At the top of kaggle_ui.py
def execute_code_cells(code_cells):
    nb = new_notebook(cells=[new_code_cell(source=code) for code in code_cells])
    ep = ExecutePreprocessor(timeout=60, kernel_name="python3")
    try:
        ep.preprocess(nb, {'metadata': {'path': './'}})
    except Exception as e:
        return nb, f"Execution error: {e}"
    return nb, None

def is_plotting_notebook(notebook_content):
    """Check if notebook contains plotting code"""
    try:
        if isinstance(notebook_content, str):
            content = json.loads(notebook_content)
        else:
            content = notebook_content
            
        plotting_keywords = ['plt.', 'plot(', 'figure(', 'show(', 'matplotlib']
        
        for cell in content:
            if cell.get('type') == 'code':
                code = cell.get('content', '')
                if any(keyword in code for keyword in plotting_keywords):
                    return True
        return False
    except:
        return False

def markdown_to_html(text):
    """Convert markdown text to HTML"""
    if not text:
        return ""
    return Markup(markdown.markdown(text))

def register_template_filters(app):
    """Register custom template filters"""
    app.jinja_env.filters['markdown'] = markdown_to_html

@app.after_request
def after_request(response):
    """Ensure all API responses are JSON"""
    if request.path.startswith('/notebook/'):
        if response.status_code >= 400:
            data = {
                "success": False,
                "message": response.get_data(as_text=True)
            }
            response.set_data(json.dumps(data))
            response.content_type = 'application/json'
    return response

@app.route("/notes")
@login_required
def notebook_manager():
    notebooks = UserNotebook.query.filter_by(user_id=current_user.id).order_by(UserNotebook.updated_at.desc()).all()
    return render_template("notebook_manager.html", notebooks=notebooks)


def execute_notebook_and_capture(path):
    with open(path) as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=60, kernel_name='python3')

    try:
        ep.preprocess(nb, {'metadata': {'path': './'}})
    except Exception as e:
        print("⚠️ Execution error:", e)

    # Save back the executed notebook
    with open(path, "w") as f:
        nbformat.write(nb, f)

    return nb



@app.route("/")
def kaggle_home():
    submissions = NotebookSubmission.query.order_by(NotebookSubmission.score.desc()).all()
    return render_template("kaggle_index.html", submissions=submissions)


@app.route("/submit", methods=["GET", "POST"])
@login_required
def submit_notebook():
    if request.method == "POST":
        file = request.files["notebook"]
        if file and file.filename.endswith(".ipynb"):
            filename = secure_filename(file.filename)
            full_path = os.path.join("submissions", f"{current_user.id}_{filename}")
            file.save(full_path)

            # ✅ Execute notebook and get outputs
            nb = execute_notebook_and_capture(full_path)

            # ✅ Optionally extract score from last cell
            score = 0.0
            for cell in reversed(nb.cells):
                if cell.cell_type == "code" and cell.outputs:
                    for output in cell.outputs:
                        if output.output_type == "execute_result":
                            try:
                                score = float(output.data["text/plain"])
                            except Exception:
                                pass
                            break

            # ✅ Create leaderboard entry
            submission = NotebookSubmission(
                user_id=current_user.id,
                notebook_filename=filename,
                score=score
            )
            db.session.add(submission)

            # ✅ Save cell contents and output into DB
            notebook_payload = []
            for cell in nb.cells:
                output = []
                if cell.cell_type == "code":
                    for o in cell.get("outputs", []):
                        if o.output_type == "stream":
                            output.append(o.text)
                        elif o.output_type == "execute_result":
                            output.append(o['data'].get('text/plain', ''))
                        elif o.output_type == "error":
                            output.append('Error: ' + '\n'.join(o['traceback']))

                notebook_payload.append({
                    "type": cell.cell_type,
                    "content": cell.source,
                    "output": output
                })

            db_notebook = UserNotebook(
                user_id=current_user.id,
                name=f"Submitted: {filename}",
                content=json.dumps(notebook_payload)
            )
            db.session.add(db_notebook)

            db.session.commit()
            return redirect(url_for("app.my_notebooks"))

        return "Invalid file format. Please upload a .ipynb file.", 400

    return render_template("submit_notebook.html")


@app.route("/editor/save", methods=["POST"])
def save_notebook_from_editor():
    data = request.get_json()
    name = data.get("name", "Untitled")
    cells = data.get("notebook", [])

    from models import Notebook
    import json

    nb = Notebook(
        name=name,
        content=json.dumps(cells),
        user_id=getattr(current_user, 'id', None)
    )
    db.session.add(nb)
    db.session.commit()

    return "✅ Notebook saved", 200




if __name__ == '__main__':
	with app.app_context():
		db.create_all()
		PendingTransactionDatabase.genisis() 
		app.run(host="0.0.0.0",port=1000)