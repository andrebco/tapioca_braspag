# coding: utf-8

import unittest

from tapioca_braspag import Braspag
import decouple

class TestTapiocaBraspag(unittest.TestCase):

    def setUp(self):
        headers = {
            "Content-Type": "application/json",
            "MerchantId": ""
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
                 "SecurityCode": "XXX",
                 "Brand": "Visa"
             }
           }
        }

        exp_resp = [
                {
                    "Code": 101,
                    "Message": "MerchantId is required"
                }
            ]

        resp = self.wrapper.sales_create().post(data=post_data)
        self.assertEqual(exp_resp, resp().data())


if __name__ == '__main__':
    unittest.main()
