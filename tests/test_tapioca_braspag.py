# coding: utf-8

import unittest
import json
import decouple

from tapioca_braspag import Braspag
from tapioca.exceptions import ClientError, ServerError

from mock import Mock, patch

class TestTapiocaBraspag(unittest.TestCase):
    merchant_id = decouple.config('MERCHANT_ID')
    merchant_key = decouple.config('MERCHANT_KEY')
    card_security_code = decouple.config('CARD_SECURITY_CODE')
    headers = {
        "Content-Type": "application/json",
        "MerchantId": merchant_id,
        "MerchantKey": merchant_key,
    }

    def setUp(self):
        self.wrapper = Braspag(headers=self.headers)

    @patch('tapioca.tapioca.requests')
    def test_post_calls_requests_with_params(self, mock_requests):
        post_data = {
           "MerchantOrderId": "2014111703",
           "Customer": {
              "Name": "Comprador Teste"
           },
           "Payment":{
             "Type": "CreditCard",
             "Amount": 15700,
             "Provider": "Simulado",
             "Installments": 1,
             "CreditCard": {
                 "CardNumber": "0000000000000001",
                 "Holder": "Teste Holder",
                 "ExpirationDate": "12/2021",
                 "SecurityCode": self.card_security_code,
                 "Brand": "Visa"
             }
           }
        }

        self.wrapper.sales_create().post(data=post_data)

        mock_requests.request.assert_called_once_with(
            u'POST',
            data=json.dumps(post_data),
            headers=self.headers,
            url=u'https://apisandbox.braspag.com.br/v2/sales/'
        )

    @patch('tapioca.tapioca.requests')
    def test_get_calls_requests_with_params(self, mock_requests):
        get_data = {
           'id': 'a_payment_id',
        }
        self.wrapper.sales_consult(**get_data).get()
        mock_requests.request.assert_called_once_with(
            u'GET',
            data=None,
            headers=self.headers,
            url='https://apiquerysandbox.braspag.com.br/v2/sales/%s' % get_data['id']
        )


    def test_post_to_api(self):
        if decouple.config('POST_TO_API', cast=bool, default=False):
            self.post_to_api()

    def post_to_api(self):
        post_data = {
           "MerchantOrderId": "2014111703",
           "Customer": {
              "Name": "Comprador Teste"
           },
           "Payment":{
             "Type": "CreditCard",
             "Amount": 15700,
             "Provider": "Simulado",
             "Installments": 1,
             "CreditCard": {
                 "CardNumber": "0000000000000001",
                 "Holder": "Teste Holder",
                 "ExpirationDate": "12/2021",
                 "SecurityCode": self.card_security_code,
                 "Brand": "Visa"
             }
           }
        }

        try:
            resp = self.wrapper.sales_create().post(data=post_data)
        except (ClientError, ServerError) as se:
            resp = se

        self.assertEquals(200, resp.status)


if __name__ == '__main__':
    unittest.main()
