import json
import unittest

from django.conf import settings
from django.test import Client
from rest_framework.test import APIClient


class TestApi(unittest.TestCase):
    def setup(self):
        self.client = APIClient()

    def test_base_url(self):
        # Test base swagger visibility
        self.client = Client()
        response = self.client.get(settings.URL_PREFIX + '/')

    def test_swagger_url(self):
        # Test swagger endpoint
        self.client = Client()
        response = self.client.get(settings.URL_PREFIX + '/#!/default/email')

    def test_post_bad_email_req(self):
        # test SMS message with invalid phone number (too long)
        self.client = Client()
        header = {'content-type': 'application/json'}
        input = {
            "personalisation": {},
            "phone_number": "+447900900123",
            "reference": "string",
            "template_id": "f33517ff-2a88-4f6e-b855-c550268ce08a"
        }
        response = self.client.post(settings.URL_PREFIX + '/api/v1/notifications/email/', json.dumps(input),
                                    'application/json', header=header)
        self.assertEqual(response.status_code, 400)

    def test_post_missing_email_req(self):
        # Test Email request that's missing email
        self.client = Client()
        input = {
            "personalisation": {
                "full name": "Name"
            },
            "reference": "string",
            "template_id": "a741fed2-7948-4b1a-b44a-fec8485ec700"
        }
        response = self.client.post(settings.URL_PREFIX + '/api/v1/notifications/email/', json.dumps(input),
                                    'application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_email_req(self):
        # Test Sending Email
        self.client = Client()
        input = {
            "email": "simulate-delivered@notifications.service.gov.uk",
            "personalisation": {
                "full name": "Name",
                "firstName": "test",
                "app_reference": "test"
            },
            "reference": "string",
            "template_id": "a741fed2-7948-4b1a-b44a-fec8485ec700"
        }
        response = self.client.post(settings.URL_PREFIX + '/api/v1/notifications/email/', json.dumps(input),
                                    'application/json')
        self.assertEqual(response.status_code, 201)

    def test_postsms_req(self):
        # test SMS message
        self.client = Client()
        header = {'content-type': 'application/json'}
        input = {
            "personalisation": {
                "first name": "Name"
            },
            "phoneNumber": "07700900111",
            "reference": "string",
            "templateId": "b2f0171a-774e-47bc-b7ef-5328758447c4"
        }
        response = self.client.post(settings.URL_PREFIX + '/api/v1/notifications/sms/', json.dumps(input), 'application/json',
                                    header=header)
        self.assertEqual(response.status_code, 201)

    def test_post_bad_sms_req(self):
        # test sending SMS request with email data
        self.client = Client()
        input = {
            "email": "matthew.styles@informed.com",
            "personalisation": {
                "full name": "Name"
            },
            "reference": "string",
            "template_id": "a741fed2-7948-4b1a-b44a-fec8485ec700"
        }
        response = self.client.post(settings.URL_PREFIX + '/api/v1/notifications/sms/', json.dumps(input), 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_PostMissingSMSReq(self):
        # test SMS message with missing phone number
        self.client = Client()
        header = {'content-type': 'application/json'}
        input = {
            "personalisation": {
                "first name": "Name"
            },
            "reference": "string",
            "template_id": "b2f0171a-774e-47bc-b7ef-5328758447c4"
        }
        response = self.client.post(settings.URL_PREFIX + '/api/v1/notifications/sms/', json.dumps(input), 'application/json',
                                    header=header)
        self.assertEqual(response.status_code, 400)
