# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PaymentToken(models.Model):
    _inherit = 'payment.token'

    cinetpay_customer_email = fields.Char(
        string="CinetPay Customer Email",
        help="L'adresse e-mail du client au moment de la création du token.",
        readonly=True
    )
    cinetpay_token_reference = fields.Char(
        string="Référence du token CinetPay",
        help="Identifiant unique du token renvoyé par CinetPay.",
        readonly=True
    )
