# coding: utf-8

import unittest

import json
import uuid
import decouple

from tapioca_braspag import Braspag, BraspagConsult

from tapioca.exceptions import ClientError, ServerError

from mock import Mock, patch

def generate_response_id():
    return uuid.uuid4()


class TestTapiocaBraspag(unittest.TestCase):
    merchant_id = decouple.config('MERCHANT_ID')
    merchant_key = decouple.config('MERCHANT_KEY')
    card_security_code = decouple.config('CARD_SECURITY_CODE')
    headers = {
        "Content-Type": "application/json",
        "MerchantId": merchant_id,
        "MerchantKey": merchant_key,
        "ResponseId": generate_response_id(),
    }

    def setUp(self):
        self.wrapper = Braspag(headers=self.headers)
        self.wrapper_consult = BraspagConsult(headers=self.headers)

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
            url=u'https://apihomolog.braspag.com.br/v2/sales/'
        )

    @patch('tapioca.tapioca.requests')
    def test_get_calls_requests_with_params(self, mock_requests):
        get_data = {
           'id': 'a_payment_id',
        }
        self.wrapper_consult.sales_consult(**get_data).get()
        mock_requests.request.assert_called_once_with(
            u'GET',
            data=None,
            headers=self.headers,
            url='https://apiqueryhomolog.braspag.com.br/v2/sales/{}'.format(
                get_data['id'])
        )

    def test_post_to_api(self):
        if decouple.config('POST_TO_API', cast=bool, default=False):
            self.post_to_api()

    def test_get_from_api(self):
        if decouple.config('POST_TO_API', cast=bool, default=False):
            self.get_from_api()

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
            sales_create = self.wrapper.sales_create().post(data=post_data)
            response = sales_create().response()
        except (ClientError, ServerError) as se:
            response = se.client().response()

        self.assertEquals(201, response.status_code)
        self.assertEquals('Created', response.reason)

    def get_from_api(self):

        try:
            merchand_sales = self.wrapper_consult.merchant_consult_sales(
                    id=self.merchant_id
                ).get()
            response = merchand_sales().response()
        except (ClientError, ServerError) as se:
            response = se.client().response()

        self.assertEquals(200, response.status_code)
        self.assertEquals('Successful', response.reason)



if __name__ == '__main__':
    unittest.main()
