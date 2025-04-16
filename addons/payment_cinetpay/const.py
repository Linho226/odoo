# -*- coding: utf-8 -*-
# Constantes pour l'intégration CinetPay

# URL de base de l'API CinetPay
API_BASE_URL = "https://api-checkout.cinetpay.com/v2"

# Endpoints
API_PAYMENT_ENDPOINT = f"{API_BASE_URL}/payment"
API_VERIFY_ENDPOINT = f"{API_BASE_URL}/payment/check"

# Statuts CinetPay retournés dans les notifications
STATUS_ACCEPTED = "ACCEPTED"
STATUS_PENDING = "PENDING"
STATUS_REFUSED = "REFUSED"
STATUS_FAILED = "FAILED"

# Codes d’erreurs standards (à adapter si CinetPay les fournit dans l’API)
ERROR_CODES = {
    '201': 'Transaction créée avec succès',
    '400': 'Requête invalide',
    '401': 'Authentification échouée',
    '500': 'Erreur serveur interne',
}

# Pour debug log / print lisibles
def get_status_label(status_code):
    labels = {
        STATUS_ACCEPTED: "Paiement accepté",
        STATUS_PENDING: "Paiement en attente",
        STATUS_REFUSED: "Paiement refusé",
        STATUS_FAILED: "Paiement échoué",
    }
    return labels.get(status_code, "Statut inconnu")
