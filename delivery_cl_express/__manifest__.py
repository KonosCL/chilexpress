# -*- coding: utf-8 -*-
# 
{
    'name': "Chile Express Delivery",
    'description': "Calcular costo de envío con Chile Express API",
    'author': 'Federico Nardi',
    'category': 'Warehouse',
    'version': '1.0',
    'depends': ['delivery', 'mail'],
    'data': [
        'views/delivery_cl_express_view.xml',
        #'views/res_config_settings_views.xml',
        'data/cl_exp_code.xml',
    ],
    'license': 'AGPL-3',
}
