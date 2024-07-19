from flask import Flask, redirect, render_template, url_for, request, session, flash, jsonify
import mysql.connector
import bcrypt
from config import read_db_config
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

import os
from datetime import timedelta, datetime, timezone
from flask_mail import Mail, Message
import secrets
import requests
from mpesaToken import *
import base64

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.getenv("SECRET_KEY", default="DefaultSecretKey")
app.permanent_session_lifetime = timedelta(minutes=15)  # Sets the session timeout to 15 minutes

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL").lower() == "true"
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)

# Mpesa configuration
SHORTCODE = os.getenv("SHORTCODE")
PASSKEY = os.getenv("PASSKEY")
MPESA_API_BASE = 'https://sandbox.safaricom.co.ke'  # Use sandbox for testing


def get_db_connection():
    try:
        db_config = read_db_config()
        conn = mysql.connector.connect(**db_config)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None
    
@app.before_request
def before_request():
    if "username" in session:
        if request.endpoint in ["login", "signup", "home"]:
            session["last_activity"] = datetime.now(timezone.utc) # Make time offset-aware


# Checks user's last activity timestamp and logs them out
@app.before_request
def check_session_timeout():
    if "username" in session and "last_activity" in session:
        last_activity = session["last_activity"].replace(tzinfo=timezone.utc) # Make time offset-aware
        excluded_endpoints = ["login", "signup", "home"]

        is_refreshed = request.args.get("refresh") == "true"

        if not is_refreshed and request.endpoint not in excluded_endpoints:
            if datetime.now(timezone.utc) - last_activity > app.permanent_session_lifetime:
                session.pop("username", None)
                return redirect(url_for("login"))
            else:
                session["last_activity"] = datetime.now(timezone.utc) # Update last activity


# @app.route("/check_session", methods=["GET"])
# def check_session():
#     if "username" in session and "last_activity" in session:
#         last_activity = session["last_activity"].replace(tzinfo=timezone.utc)
#         if datetime.now(timezone.utc) - last_activity > app.permanent_session_lifetime:
#             session.pop("username"), None
#             return jsonify("session_expired")
#         else:
#             return jsonify("session_active")
#     else:
#         return jsonify("session_active")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        # print("Received POST request for signup")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        if username_exists(username):
            flash("Username already exists. Please choose another username.", "error")
            return render_template("signup.html", error="Registration failed")

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        confirmation_token = secrets.token_urlsafe(30)
        token_expiration = datetime.now() + timedelta(hours=2)
        send_confirmation_email(email, confirmation_token)

        try:
            conn = get_db_connection()
            if conn is None:
                print("Error connecting to the database.")
                return
            cursor = conn.cursor()

            query = "INSERT INTO users (email, username, password, confirmation_token, is_confirmed, token_expiration) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (email, username, hashed_password, confirmation_token, False, token_expiration))
            conn.commit()

            print(f"Received: Email - {email}, Username - {username}, Password - {password}")

        

            return redirect(url_for("login"))
        except Exception as e:
            print(f"Error registering user: {e}")
            flash("Error registering user. Please try again.", "error")
            return render_template("signup.html", error="Registration failed")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template("signup.html")


# Function to confirm email used in registration using a link
def send_confirmation_email(email, confirmation_token):
    try:
        print(f"Preparing to send email to {email} - Confirmation Token: {confirmation_token}")
        # print(f"Email to {email} - Confirmation Token: {confirmation_token}")
        subject = "Confirm your Email"
        body = f"Click the following link to confirm your email: {url_for('confirm_email', token=confirmation_token, _external=True)}"

        message = Message(subject, recipients=[email], body=body)
        mail.send(message)
        flash("Confirmation email sent successfully.", "success")
    except Exception as e:
        flash(f"Falied to send confirmation email. Error: {str(e)}", "error")
        # print(f"Error sending email: {e}")


@app.route("/confirm_email/<token>")
def confirm_email(token):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT username, token_expiration FROM users WHERE confirmation_token = %s"
        cursor.execute(query, (token,))
        result = cursor.fetchone()

        if result:
            username, token_expiration = result
            if datetime.utcnow() > token_expiration.replace(tzinfo=None):
                flash("The confirmation link has expired. Please request a new one.", "error")
                return render_template("confirm_email.html", success=False, error_message="The confirmation link has expired")
            
            # This marks the user as confirmed
            cursor.execute("UPDATE users SET is_confirmed = TRUE, token_expiration = NULL WHERE username = %s", (username,))
            conn.commit()
            flash("Email confirmed successfully. You can log in.", "success")
            return redirect(url_for("login"))
        else:
            flash("Invalid confirmation token.", "error")
            return render_template("confirm_email.html", success=False, error_message="Invalid confirmation token.")
    except Exception as e:
        print(f"Error confirming email: {e}")
        flash("Error confirming email. Please try again.", "error")
        return render_template("confirm_email.html", success=False, error_message="Error confirming email. Please try again.")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

        return redirect(url_for("login"))


def username_exists(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT username FROM users WHERE username = %s"
        cursor.execute(query,(username,))
        result = cursor.fetchone()

        return result is not None
    
    except Exception as e:
        print(f"Error checking if username exists: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def user_authenticated(username, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT password, is_confirmed FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        # if result:
        #     hashed_password, is_confirmed = result
        #     if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")) and is_confirmed:
        #         return True

        if result:
            return True
           
        conn.close()
    except Exception as e:
        print(f"Error authenticating user: {e}")
    return False


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if user_authenticated(username, password):
            session["username"] = username
            session["last_activity"] = datetime.now(timezone.utc) # Set last activity
            return redirect(url_for("home", username=username))
        else:
            flash("Session expired.Please log in again.", "info")
            return render_template("login.html", error="Authentication failed")
        
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/home/<username>")
def home(username):
    if "username" in session and session["username"] == username:
        return render_template("app.html", username=username)
    else:
         return redirect(url_for("login"))
    

# Mpesa Payment Routes
def initiate_stk_push(phone_number, amount, account_reference, transaction_desc):
    access_token = get_access_token()
    api_url = f'{MPESA_API_BASE}/mpesa/stkpush/v1/processrequest'
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(f'{SHORTCODE}{PASSKEY}{timestamp}'.encode()).decode('utf-8')
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Remove + from phone number
    phone_number = phone_number.lstrip('+')

    callback_url = url_for('mpesa_callback', _external=True)
    print(callback_url)
    
    payload = {
        'BusinessShortCode': SHORTCODE,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount,
        'PartyA': phone_number,
        'PartyB': SHORTCODE,
        'PhoneNumber': phone_number,
        'CallBackURL': url_for('mpesa_callback', _external=True),  # Update with your callback URL
        'AccountReference': account_reference,
        'TransactionDesc': transaction_desc
    }
    
    print("Sending STK Push request with payload:", payload)
    response = requests.post(api_url, json=payload, headers=headers)
    print("MPesa response status code:", response.status_code)  # Add this line to debug
    print("MPesa response body:", response.text)
    return response.json()

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    phone_number = data['phone_number']
    amount = data['amount']
    account_reference = 'Order123'
    transaction_desc = 'Payment for order'
    
    response = initiate_stk_push(phone_number, amount, account_reference, transaction_desc)
    # print("Checkout response", response)
    if response.get('errorCode'):
        return jsonify({'error': response.get('errorMessage')}), 400
    return jsonify(response)

@app.route('/mpesa_callback', methods=['POST'])
def mpesa_callback():
    data = request.json
    # Process the callback data here (e.g., update order status, save transaction details)
    print(data)
    return jsonify({'ResultCode': 0, 'ResultDesc': 'Accepted'})


if __name__ == '__main__':
    app.run(debug=True)
