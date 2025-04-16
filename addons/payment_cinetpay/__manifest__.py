{
    'name': 'Payment CinetPay',
    'version': '1.0',
    'category': 'Payment',
    'summary': 'Module de paiement via CinetPay pour Odoo',
    'description': """
        Ce module permet d'intégrer la passerelle de paiement CinetPay dans Odoo,
        permettant aux utilisateurs de traiter les paiements via cette plateforme.
    """,
    'author': 'Sunsoft',
    'website': 'https://www.sunsoft.com',
    'depends': ['payment'],
    'data': [
        'views/payment_provider_form.xml',  # Formulaire de configuration du fournisseur de paiement
        #'views/payment_transaction_view.xml',  # Vue pour afficher les transactions de paiement
    ],
    'assets': {
        'web.assets_frontend': [
            'payment_cinetpay/static/src/js/payment_form.js',  # Script JavaScript pour gérer le formulaire de paiement
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
