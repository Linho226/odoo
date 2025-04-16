from odoo import http
from odoo.http import request
import time
import json
import requests

class CinetpayController(http.Controller):

    @http.route('/shop/buy_now/<int:product_id>', type='http', auth='public', website=True)
    def buy_now_form(self, product_id, **kwargs):
        product = request.env['product.product'].sudo().browse(product_id)
        if not product.exists():
            return request.render('website.404')

        return request.render('website_sale.buy_now_form', {
            'product': product
        })

    @http.route('/shop/submit_buy_now', type='http', auth='public', website=True, csrf=True, methods=['POST'])
    def submit_buy_now(self, **post):
        try:
            # 1. Récupération des données du formulaire
            product_id = int(post.get('product_id'))
            name = post.get('name')
            surname = post.get('surname')
            email = post.get('email')
            phone = post.get('phone')
            address = post.get('address')
            city = post.get('city')
            country = post.get('country') or "CM"
            state = post.get('state') or "CM"
            zip_code = post.get('zip_code')

            # Vérification des données
            if not all([product_id, name, surname, email, phone]):
                return request.render('website.404', {'error': 'Champs obligatoires manquants'})

            # 2. Récupération du produit
            product = request.env['product.product'].sudo().browse(product_id)
            if not product.exists():
                return request.render('website.404', {'error': 'Produit introuvable'})

            amount = product.lst_price
            trans_id = str(int(time.time()))  # Transaction ID unique

            # 3. Construction des données pour CinetPay
            cinetpay_data = {
                "apikey": "178011212167efc7628d1cf3.91649419",
                "site_id": "105891419",
                "transaction_id": trans_id,
                "amount": amount,
                "currency": "XOF",
                "alternative_currency": "",
                "description": f"Achat de {product.name}",
                "customer_id": str(trans_id),
                "customer_name": name,
                "customer_surname": surname,
                "customer_email": email,
                "customer_phone_number": phone,
                "customer_address": address,
                "customer_city": city,
                "customer_country": country,
                "customer_state": state,
                "customer_zip_code": zip_code,
                "notify_url": "https://votre-domaine.com/cinetpay/notify",
                "return_url": "https://votre-domaine.com/shop/payment_return",
                "channels": "ALL",
                "metadata": "user1",
                "lang": "FR",
                "invoice_data": {
                    "Donnee1": "",
                    "Donnee2": "",
                    "Donnee3": ""
                }
            }

            headers = {'Content-Type': 'application/json'}
            response = requests.post("https://api-checkout.cinetpay.com/v2/payment", headers=headers, data=json.dumps(cinetpay_data))

            if response.status_code == 200:
                res_data = response.json()
                payment_url = res_data.get('data', {}).get('payment_url')
                if payment_url:
                    # Astuce : Rediriger vers une page HTML qui ouvre une fenêtre automatiquement
                    return request.render('website_sale.redirect_to_payment', {
                        'payment_url': payment_url
                    })
                else:
                    return request.render('website.404', {'error': 'Lien de paiement introuvable'})
            else:
                return request.render('website.404', {'error': 'Erreur lors de la création du paiement'})

        except Exception as e:
            return request.render('website.404', {'error': str(e)})
