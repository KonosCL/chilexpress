# -*- coding: utf-8 -*-
# 
from odoo import api, SUPERUSER_ID
from . import models



def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['delivery.carrier'].search([
        ('delivery_type', '=', 'clexp')
    ]).write({'delivery_type': 'fixed', 'fixed_price': 0})
