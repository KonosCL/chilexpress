# -*- coding: utf-8 -*-
#from .dhl_request import DHLProvider
import logging
import requests
from odoo import models, fields, _

_logger = logging.getLogger(__name__)

class CodCity(models.Model):
	_inherit = 'res.city'
	cod_clexp = fields.Char(string='Codigo Chile Express')

class Providerclexp(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(selection_add=[('clexp', "Chile Express")])
    clexp_API = fields.Char(string="Chile Express API key")

    def __init__(self, prod_environment, debug_logger):
        self.debug_logger = debug_logger
        if not prod_environment:
            self.url = 'https://testservices.wschilexpress.com/rating/api/v1.0/rates/courier'
        else:
            self.url = 'https://testservices.wschilexpress.com/rating/api/v1.0/rates/courier'

    #se cambió de rate_shipment a clexp_rate_shipment para no interferir con los demás proveedores
    def clexp_rate_shipment(self, order):
        url = 'https://testservices.wschilexpress.com/rating/api/v1.0/rates/courier'
        headers = {
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': '1e94a388c79d4616967f9f7009a81963',
        }


        orden = self.env['sale.order'].search([('id', '=', 42)], limit=1)

        max_length=0
        max_width=0
        max_height=0
        peso=0

        for line in orden.order_line:
            #_logger.warning(line.product_id.length)
            #_logger.warning(line.product_id.width)
            #_logger.warning(line.product_id.height)
            #_logger.warning(line.product_id.weight)

            if (int(line.product_id.length)*int(line.product_uom_qty))>max_length:
                max_length=(int(line.product_id.length)*int(line.product_uom_qty))
            if int(line.product_id.width)>max_width:
                max_width=int(line.product_id.width)
            if int(line.product_id.height)>max_height:
                max_height=int(line.product_id.height)
            peso+=float(line.product_id.weight)*int(line.product_uom_qty)

        #_logger.warning(max_length)
        #_logger.warning(max_width)
        #_logger.warning(max_height)
        #_logger.warning(peso)


        caja={
            "originCountyCode": self.env.user.company_id.city_id.cod_clexp,
            "destinationCountyCode": orden.partner_shipping_id.city_id.cod_clexp,
            "package": {
                "weight": peso,
                "height": max_height,
                "width": max_width,
                "length": max_length
            },
            "productType": 3,
            "contentType": 1,
            "declaredWorth": "1000",
            "deliveryTime": 0
        }

        url="https://testservices.wschilexpress.com/rating/api/v1.0/rates/courier"
        respuesta = requests.post(url, json=caja, headers=headers)
        como_json = respuesta.json()

        try:
            return {'success': True,
                'price':como_json["data"]["courierServiceOptions"][0]["serviceValue"],
                'error_message': False,
                'warning_message': False}
        except:
            return {'success': False,
                'price':"0",
                'error_message': "Error",
                'warning_message': "Error"}
