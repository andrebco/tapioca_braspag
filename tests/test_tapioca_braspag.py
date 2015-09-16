# coding: utf-8

import unittest
import decouple

from tapioca_braspag import Braspag
from tapioca.exceptions import ClientError

class TestTapiocaBraspag(unittest.TestCase):
    merchand_id = decouple.config('MERCHAND_ID', default='')
    card_security_code = decouple.config('CARD_SECURITY_CODE')

    def setUp(self):
        headers = {
            "Content-Type": "application/json",
            "MerchantId": self.merchand_id,
        }
        self.wrapper = Braspag(headers=headers)

    def test_post_return_200(self):
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
                 "CardNumber": "0000.0000.0000.0001",
                 "Holder": "Teste Holder",
                 "ExpirationDate": "12/2021",
                 "SecurityCode": self.card_security_code,
                 "Brand": "Visa"
             }
           }
        }

        try:
            resp = self.wrapper.sales_create().post(data=post_data)
        except ClientError as ce:
            resp = ce.client().response()

        self.assertEqual('[{"Code":101,"Message":"MerchantId is required"}]', 
                         resp.content)


if __name__ == '__main__':
    unittest.main()
