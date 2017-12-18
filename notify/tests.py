import json
import sys
import unittest

from django.test import Client
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class TestApi(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_BaseURL(self):
        #Test base swagger visibility
        response = self.client.get('/')
        #self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_SwaggerURL(self):
        #Test swagger endpoint
        response = self.client.get('/#!/default/email')
        #self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_setApiKey(self):
        #Test updating the APi Key
        self.client = Client()
        header = {'content-type': 'application/json'}
        input = {
            "apiKey": "dev_api-7c51af0f-8720-4315-9d67-b4f94d7531e0-df9b0c2e-6d50-4102-ae62-9a24cde656cc"
        }
        response = self.client.put('/notify-gateway/api/v1/notifications/api-key/' , json.dumps(input), 'application/json' , header=header)
        self.assertEqual(response.status_code, 200)
    def test_badSetApiKey(self):
        #Update the API key, with an empty string
        self.client = Client()
        header = {'content-type': 'application/json'}
        input = {
            "apiKey": ""
        }
        response = self.client.put('/notify-gateway/api/v1/notifications/api-key/' , json.dumps(input), 'application/json' , header=header)
        #This test is meant to fail
        self.assertEqual(response.status_code, 400)

    def test_PostBadEmailReq(self):
        # test SMS message with invalid phone number (too long)
        self.client = Client()
        header = {'content-type': 'application/json'}
        input = {
            "personalisation": {},
            "phoneNumber": "+447900900123",
            "reference": "string",
            "templateId": "f33517ff-2a88-4f6e-b855-c550268ce08a"
            }
        response = self.client.post('/notify-gateway/api/v1/notifications/email/' , json.dumps(input), 'application/json', header=header)
        self.assertEqual(response.status_code, 400)
    def test_PostMissingEmailReq(self):
        #Test Email request that's missing email
        self.client = Client()
        input = {
            "personalisation": {
            "full name":"Name"
        },
            "reference": "string",
            "templateId": "a741fed2-7948-4b1a-b44a-fec8485ec700"
        }
        response = self.client.post('/notify-gateway/api/v1/notifications/email/' , json.dumps(input), 'application/json')
        self.assertEqual(response.status_code, 400)


    def test_PostEmailReq(self):
        #Test Sending Email
        self.client = Client()
        input = {
            "email": "matthew.styles@informed.com",
            "personalisation": {
            "full name":"Name"
        },
            "reference": "string",
            "templateId": "a741fed2-7948-4b1a-b44a-fec8485ec700"
        }
        response = self.client.post('/notify-gateway/api/v1/notifications/email/' , json.dumps(input), 'application/json')
        self.assertEqual(response.status_code, 201)
    
    def test_PostSMSReq(self):
        #test SMS message 
        self.client = Client()
        header = {'content-type': 'application/json'}
        input = {
            "personalisation": {
            "first name":"Name"
        },
            "phoneNumber": "07557986930",
            "reference": "string",
            "templateId": "b2f0171a-774e-47bc-b7ef-5328758447c4"
            }
        response = self.client.post('/notify-gateway/api/v1/notifications/sms/' , json.dumps(input), 'application/json', header=header)
        self.assertEqual(response.status_code, 201)
    def test_PostBadSMSReq(self):
        #test sending SMS request with email data
        self.client = Client()
        input = {
            "email": "matthew.styles@informed.com",
            "personalisation": {
            "full name":"Name"
        },
            "reference": "string",
            "templateId": "a741fed2-7948-4b1a-b44a-fec8485ec700"
        }
        response = self.client.post('/notify-gateway/api/v1/notifications/sms/' , json.dumps(input), 'application/json')
        self.assertEqual(response.status_code, 400)
    def test_PostMissingSMSReq(self):
        #test SMS message with missing phone number
        self.client = Client()
        header = {'content-type': 'application/json'}
        input = {
            "personalisation": {
            "first name":"Name"
        },
            "reference": "string",
            "templateId": "b2f0171a-774e-47bc-b7ef-5328758447c4"
            }
        response = self.client.post('/notify-gateway/api/v1/notifications/sms/' , json.dumps(input), 'application/json', header=header)
        self.assertEqual(response.status_code, 400)

