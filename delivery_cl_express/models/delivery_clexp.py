import logging
import requests
from odoo import models, fields, _

_logger = logging.getLogger(__name__)


class CodCity(models.Model):
    _inherit = 'res.city'
    cod_clexp = fields.Char(string='Chilexpress Code')


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(selection_add=[('clexp', "Chilexpress")])
    clexp_api = fields.Char(string="Chile Express API key")

    # def __init__(self, prod_environment, debug_logger):
    #     self.debug_logger = debug_logger
    #     if not prod_environment:
    #         self.url = 'https://testservices.wschilexpress.com/rating/api/v1.0/rates/courier'
    #     else:
    #         self.url = 'https://testservices.wschilexpress.com/rating/api/v1.0/rates/courier'

    def rate_shipment(self, order):
        url = 'https://testservices.wschilexpress.com/rating/api/v1.0/rates/courier'

        headers = {
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': '1e94a388c79d4616967f9f7009a81963',
        }
        # hardcoded order for testing purposes
        order = self.env['sale.order'].browse(42)
        
        max_length = 0
        max_width = 0
        max_height = 0
        weight = 0

        for line in order.order_line:
            extended_length = int(round(line.product_id.length * line.product_uom_qty, 0))
            max_length = extended_length if extended_length > max_length else max_length
            max_width = int(round(line.product_id.width, 0)) if int(round(line.product_id.width, 0)) > max_width else max_width
            max_height = int(round(line.product_id.height, 0)) if int(round(line.product_id.height, 0)) > max_height else max_height

            weight += line.product_id.weight * line.product_uom_qty

        weight = int(round(weight, 0))
        caja = {
            "originCountyCode": self.env.user.company_id.city_id.cod_clexp,
            "destinationCountyCode": order.partner_shipping_id.city_id.cod_clexp,
            "package": {
                "weight": weight,
                "height": max_height,
                "width": max_width,
                "length": max_length
            },
            "productType": 3,
            "contentType": 1,
            "declaredWorth": "1000",
            "deliveryTime": 0
        }
        try:
            res = requests.post(url, json=caja, headers=headers)
            res.raise_for_status()
        except Exception as e:
            return {
                'success': False,
                'price': "0",
                'error_message': e,
                'warning_message': "Error"}
        json_data = res.json()
        return {
            'success': True,
            'price': json_data["data"]["courierServiceOptions"][0]["serviceValue"],
            'error_message': False,
            'warning_message': False}
