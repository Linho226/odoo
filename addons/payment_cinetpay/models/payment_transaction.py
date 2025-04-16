# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

from werkzeug import urls
from odoo import models, _, fields
from odoo.exceptions import ValidationError, UserError

from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment_cinetpay import const

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """ Préparation des valeurs spécifiques à CinetPay pour le formulaire de redirection. """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'cinetpay':
            return res

        base_url = self.provider_id.get_base_url()
        return_url = urls.url_join(base_url, CinetpayController._return_url)
        notify_url = urls.url_join(base_url, CinetpayController._notify_url)

        payload = {
            'amount': self.amount,
            'currency': self.currency_id.name,
            'transaction_id': self.reference,
            'return_url': return_url,
            'notify_url': notify_url,
            'customer_name': self.partner_name,
            'customer_email': self.partner_email,
            'description': f"Paiement pour {self.reference}",
            'site_id': self.provider_id.cinetpay_site_id,
            'apikey': self.provider_id.cinetpay_apikey,
        }

        response = self.provider_id._cinetpay_make_request('payment', payload=payload)
        _logger.info("Réponse CinetPay INIT : %s", pprint.pformat(response))

        if response.get('code') != '201':
            raise ValidationError(_("CinetPay: Erreur de création de transaction : %s", response.get('message')))

        return {
            'api_url': response['data']['payment_url'],
        }

    def _process_notification_data(self, notification_data):
        """ Traitement des notifications CinetPay. """
        super()._process_notification_data(notification_data)
        if self.provider_code != 'cinetpay':
            return

        self.ensure_one()
        _logger.info("Notification reçue de CinetPay : %s", pprint.pformat(notification_data))

        tx_ref = notification_data.get('transaction_id')
        status = notification_data.get('status')

        if self.reference != tx_ref:
            raise ValidationError(_("CinetPay: Référence transaction non valide."))

        if status == 'ACCEPTED':
            self._set_done()
        elif status == 'PENDING':
            self._set_pending()
        elif status == 'REFUSED':
            self._set_canceled()
        else:
            self._set_error(_("Statut de paiement inconnu : %s", status))

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Récupération de la transaction depuis les données CinetPay. """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'cinetpay' or tx:
            return tx

        tx_ref = notification_data.get('transaction_id')
        if not tx_ref:
            raise ValidationError(_("CinetPay: Référence manquante dans la notification."))

        tx = self.search([('reference', '=', tx_ref), ('provider_code', '=', 'cinetpay')])
        if not tx:
            raise ValidationError(_("CinetPay: Aucune transaction trouvée avec la référence %s.", tx_ref))

        return tx
