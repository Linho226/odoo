# payment_cinetpay/controllers/main.py
from odoo import http
from odoo.http import request
import json
import random
import requests

class CinetpayController(http.Controller):

    @http.route(['/shop/buy_now/<int:product_id>'], type='http', auth="public", website=True)
    def buy_now_form(self, product_id, **kwargs):
        product = request.env['product.product'].browse(product_id)
        return request.render('payment_cinetpay.buy_now_form', {
            'product': product
        })

    @http.route(['/shop/buy_now/process'], type='http', auth="public", website=True, csrf=False)
    def buy_now_process(self, **post):
        transaction_id = str(random.randint(10000000, 99999999))
        cinetpay_payload = {
            "apikey": "178011212167efc7628d1cf3.91649419",
            "site_id": "105891419",
            "transaction_id": transaction_id,
            "amount": float(post.get('amount')),
            "currency": "XOF",
            "description": "Achat produit %s" % post.get('product_name'),
            "customer_id": post.get("customer_id"),
            "customer_name": post.get("customer_name"),
            "customer_surname": post.get("customer_surname"),
            "customer_email": post.get("customer_email"),
            "customer_phone_number": post.get("customer_phone"),
            "customer_address": post.get("customer_address"),
            "customer_city": post.get("customer_city"),
            "customer_country": post.get("customer_country"),
            "customer_state": post.get("customer_state"),
            "customer_zip_code": post.get("customer_zip"),
            "notify_url": "https://webhook.site/d1dbbb89-52c7-49af-a689-b3c412df820d",
            "return_url": "https://www.ieinnova.net/",
            "channels": "ALL",
            "metadata": "user1",
            "lang": "FR"
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            'https://api-checkout.cinetpay.com/v2/payment',
            data=json.dumps(cinetpay_payload),
            headers=headers
        )

        if response.status_code == 200:
            payment_data = response.json()
            return request.redirect(payment_data.get("data", {}).get("payment_url", "/"))
        else:
            return request.render('payment_cinetpay.payment_error', {'error': response.text})
