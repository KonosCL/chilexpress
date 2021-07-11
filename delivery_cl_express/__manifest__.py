{
    'name': "Chilexpress Delivery",
    'version': '1.0',
    'category': 'Warehouse',
    'sequence': 12,
    'author': 'Federico Nardi',
    'description': """
Chilexpress Connector
=====================
Calculate the delivery cost using Chilexpress API
""",
    'website': '',
    'depends': ['delivery', 'mail'],
    'external_dependencies': {
        'python': [
        ],
    },
    'data': [
        'views/delivery_cl_express_view.xml',
        #'views/res_config_settings_views.xml',
        'data/cl_exp_code.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
    'license': 'LGPL-3',
}

