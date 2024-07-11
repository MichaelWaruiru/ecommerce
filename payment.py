from app import *
import paypalrestsdk

paypalrestsdk.configure({
    "mode": "sandbox", # Sandbox for testing, live for production
    "client_id": os.getenv("PAYPAL_CLIENT_ID"),
    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET")
})

# Route for payment checkout
@app.route("/checkout", methods=["POST"])
def checkout():
    cart = session.get("cart", [])
    total = sum(item["price"] * item["quantity"] for item in cart)

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": url_for('payment_execute', _external=True),
            "cancel_url": url_for('payment_cancel', _external=True)
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": item['name'],
                    "sku": item['name'],
                    "price": str(item['price']),
                    "currency": "USD",
                    "quantity": item['quantity']
                } for item in cart]
            },
            "amount": {
                "total": str(total),
                "currency": "USD"
            },
            "description": "Purchase from your store."
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                return redirect(approval_url)
    else:
        flash("Error creating PayPal payment.")
        print("Error making PayPal payment")
        return redirect(url_for('home', username=session.get("username")))

@app.route('/payment_execute', methods=['GET'])
def payment_execute():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        flash("Payment successful.")
        session.pop('cart', None)  # Clear the cart
        return redirect(url_for('home', username=session.get("username")))
    else:
        flash("Payment failed.")
        print("Payment failed")
        return redirect(url_for('home', username=session.get("username")))

@app.route('/payment_cancel', methods=['GET'])
def payment_cancel():
    flash("Payment cancelled.")
    return redirect(url_for('home', username=session.get("username")))


# Example usage in a view function
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_name = request.form['product_name']
    product_price = float(request.form['product_price'])
    quantity = int(request.form['quantity'])
    session['cart'].append({
        'name': product_name,
        'price': product_price,
        'quantity': quantity
    })
    return redirect(url_for('home', username=session.get("username")))
