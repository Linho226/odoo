# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import requests
from werkzeug.urls import url_join

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment.const import REPORT_REASONS_MAPPING

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('cinetpay', "CinetPay")], ondelete={'cinetpay': 'set default'}
    )
    cinetpay_api_key = fields.Char(
        string="CinetPay API Key",
        help="Clé API fournie par CinetPay pour authentifier les requêtes.",
        required_if_provider='cinetpay',
    )
    cinetpay_site_id = fields.Char(
        string="CinetPay Site ID",
        help="Identifiant de site fourni par CinetPay.",
        required_if_provider='cinetpay',
    )
    cinetpay_notify_url = fields.Char(
        string="Webhook / Notify URL",
        help="URL de callback pour les notifications de CinetPay.",
    )

    # === COMPUTED METHODS ===

    def _compute_feature_support_fields(self):
        """Active certaines fonctionnalités pour CinetPay."""
        super()._compute_feature_support_fields()
        self.filtered(lambda p: p.code == 'cinetpay').update({
            'support_tokenization': False,
        })


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    cinetpay_webhook_secret = fields.Char('CinetPay Webhook Secret', help="Secret key for CinetPay webhook verification")


    # === BUSINESS METHODS ===

    @api.model
    def _get_compatible_providers(self, *args, is_validation=False, report=None, **kwargs):
        """Exclut CinetPay pour la validation de carte (tokenization)."""
        providers = super()._get_compatible_providers(
            *args, is_validation=is_validation, report=report, **kwargs
        )

        if is_validation:
            unfiltered_providers = providers
            providers = providers.filtered(lambda p: p.code != 'cinetpay')
            payment_utils.add_to_report(
                report,
                unfiltered_providers - providers,
                available=False,
                reason=REPORT_REASONS_MAPPING['validation_not_supported'],
            )

        return providers

    def _get_supported_currencies(self):
        """Devise supportée par CinetPay."""
        supported_currencies = super()._get_supported_currencies()
        if self.code == 'cinetpay':
            supported_currencies = supported_currencies.filtered(
                lambda c: c.name in ['XOF', 'XAF', 'CDF', 'GNF']
            )
        return supported_currencies

    def _cinetpay_make_request(self, endpoint, payload=None, method='POST'):
        """Effectue une requête à l'API de CinetPay.

        :param str endpoint: L’URL ou endpoint visé (ex: `/v2/payment`).
        :param dict payload: Données à envoyer à l’API.
        :param str method: Méthode HTTP (POST/GET).
        :return dict: Résultat JSON.
        :raise ValidationError: En cas d'erreur de communication.
        """
        self.ensure_one()

        url = url_join('https://api-checkout.cinetpay.com', endpoint)
        headers = {'Content-Type': 'application/json'}

        try:
            if method == 'GET':
                response = requests.get(url, params=payload, headers=headers, timeout=10)
            else:
                response = requests.post(url, json=payload, headers=headers, timeout=10)

            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                _logger.exception(
                    "Erreur API CinetPay à %s avec données :\n%s", url, pprint.pformat(payload),
                )
                raise ValidationError("CinetPay : " + _(
                    "Erreur API : '%s'", response.json().get('message', '')
                ))

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            _logger.exception("Connexion impossible à l’API CinetPay à %s", url)
            raise ValidationError("CinetPay : " + _("Échec de connexion à l’API."))

        return response.json()

    def _get_default_payment_method_codes(self):
        """Retourne les méthodes de paiement par défaut pour CinetPay."""
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'cinetpay':
            return default_codes
        return [{'code': 'cinetpay', 'name': "CinetPay Checkout"}]
