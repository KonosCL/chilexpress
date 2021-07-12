import logging
import requests
from odoo import models, fields, _

_logger = logging.getLogger(__name__)

CHILEXPRESS_URL = {
    'test': 'https://testservices.wschilexpress.com/rating/api/v1.0/rates/courier',
    'prd': 'https://testservices.wschilexpress.com/rating/api/v1.0/rates/courier',  # poner la url de produccion
}


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    # these values could be located in the company, as currency_rate_live
    delivery_type = fields.Selection(selection_add=[('chilexpress', "Chilexpress")])
    chilexpress_api_test = fields.Char(string="Chilexpress Test API key")
    chilexpress_api_prd = fields.Char(string="Chilexpress Production API key")
    chilexpress_url = fields.Selection(
        [('test', 'Test'), ('prd', 'Production')], string='Chilexpress Connection Type', default='test')

    def chilexpress_rate_shipment(self, order):
        self.ensure_one()
        api_token = getattr(self, 'chilexpress_api_%s' % self.delivery_type)
        headers = {
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': api_token,  # '1e94a388c79d4616967f9f7009a81963',
        }

        max_length = 0
        max_width = 0
        max_height = 0
        weight = 0

        for line in order.order_line:
            extended_length = int(round(line.product_id.length * line.product_uom_qty, 0))
            max_length = extended_length if extended_length > max_length else max_length
            max_width = int(round(line.product_id.width, 0)) if int(round(line.product_id.width, 0)) > max_width \
                else max_width
            max_height = int(round(line.product_id.height, 0)) if int(round(line.product_id.height, 0)) > max_height \
                else max_height
            weight += line.product_id.weight * line.product_uom_qty

        weight = int(round(weight, 0))
        data = {
            'originCountyCode': self.env.user.company_id.city_id.cod_clexp,
            'destinationCountyCode': order.partner_shipping_id.city_id.cod_clexp,
            'package': {
                'weight': weight,
                'height': max_height,
                'width': max_width,
                'length': max_length
            },
            'productType': 3,
            'contentType': 1,
            'declaredWorth': '1000',
            'deliveryTime': 0
        }
        try:
            res = requests.post(CHILEXPRESS_URL[self.chilexpress_url], json=data, headers=headers)
            res.raise_for_status()
        except Exception as e:
            return {
                'success': False,
                'price': '0',
                'error_message': e,
                'warning_message': 'Error'}
        json_data = res.json()
        return {
            'success': True,
            'price': float(json_data['data']['courierServiceOptions'][0]['serviceValue']),
            'error_message': False,
            'warning_message': False}
