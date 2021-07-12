from odoo import models, fields, _


class CodCity(models.Model):
    _inherit = 'res.city'

    cod_clexp = fields.Char(string='Chilexpress Code')
