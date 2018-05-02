"""
View logic for managing notifications API invocations
"""

import logging
import traceback

from django.conf import settings
from django.http import JsonResponse
from notifications_python_client.errors import HTTPError
from notifications_python_client.notifications import NotificationsAPIClient
from rest_framework import status
from rest_framework.decorators import api_view

from .utilities import Utilities
from .serializers import EmailSerializer, NotifySerializer, SmsSerializer

# Initiate logger
log = logging.getLogger('django.server')

# Get notify api key from settings file
NOTIFICATIONS_CLIENT = NotificationsAPIClient(settings.NOTIFY_API_KEY)


@api_view(['PUT'])
def change_api_key(request):
    """
    This method is used to update the notify api key
    :param request: The api key is the only parameter passed in via the request
    :return: A JsonResponse with the status code, and a message
    """
    # This method is for updating the API key
    try:
        mapped_json_request = Utilities.convert_json_to_python_object(request.data)
        serializer = NotifySerializer(data=mapped_json_request)
        if serializer.is_valid():
            # API key set
            global NOTIFICATIONS_CLIENT
            NOTIFICATIONS_CLIENT = NotificationsAPIClient(serializer.data['api_key'])
            return JsonResponse({"message": "Api key successfully updated"}, status=200)
        err = __format_error(serializer.errors)
        log.error("Django serialization error: " + err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error": "Bad Request", }, status=status.HTTP_400_BAD_REQUEST)
    except HTTPError as ex:
        exception_data = traceback.format_exc().splitlines()
        exception_array = [exception_data[-3:]]
        log.error(exception_array)
        return JsonResponse(ex.message, status=ex.status_code, safe=False)
    except Exception as ex:
        exceptiondata = traceback.format_exc().splitlines()
        exceptionarray = [exceptiondata[-3:]]
        log.error(exceptionarray)
        return JsonResponse(ex.__dict__, status=500)


@api_view(['POST'])
def send_email(request):
    """
    This method handles the send Email requests and responses
    :param request: All of the necessary parameters for a successful email Notify request are passed in via the request
    :return: A JsonResponse with the status code and message
    """
    try:
        mapped_json_request = Utilities.convert_json_to_python_object(request.data)
        serializer = EmailSerializer(data=mapped_json_request)
        if serializer.is_valid():
            # call method to send email
            return __send_email_via_notify(serializer.data)
        err = __format_error(serializer.errors)
        log.error("Django serialization error: " + err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
    except HTTPError as ex:
        exceptiondata = traceback.format_exc().splitlines()
        exceptionarray = [exceptiondata[-3:]]
        log.error(exceptionarray)
        return JsonResponse(ex.message, status=ex.status_code, safe=False)
    except Exception as ex:
        exceptiondata = traceback.format_exc().splitlines()
        exceptionarray = [exceptiondata[-3:]]
        log.error(exceptionarray)
        return JsonResponse(ex.__dict__, status=500)


@api_view(['POST'])
def send_sms(request):
    """
    This method handles the send SMS request and responses, and validates them.
    :param request: All of the necessary parameters for a successful SMS Notify request are passed in via the request
    :return: A JsonResponse with the status code and message
    """
    try:
        mapped_json_request = Utilities.convert_json_to_python_object(request.data)
        serializer = SmsSerializer(data=mapped_json_request)
        if serializer.is_valid():
            return __send_sms_via_notify(serializer.data)
        err = __format_error(serializer.errors)
        log.error("Django serialization error: " + err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
    except HTTPError as ex:
        exceptiondata = traceback.format_exc().splitlines()
        exceptionarray = [exceptiondata[-3:]]
        log.error(exceptionarray)
        return JsonResponse(ex.message, status=ex.status_code, safe=False)
    except Exception as ex:
        exceptiondata = traceback.format_exc().splitlines()
        exceptionarray = [exceptiondata[-3:]]
        log.error(exceptionarray)
        return JsonResponse(ex.__dict__, status=500)


def __send_email_via_notify(data):
    """
    This method actually makes the post request to the Notify endpoint
    :param data: All of the necessary parameters for a successful SMS Notify request are passed in via the request
    :return: The a 201 and the notify id if the request to Notify is successful
    """
    # Read serialized email info
    email = data['email']
    template_id = data['template_id']
    if 'reference' in data:
        reference = data['reference']
    else:
        reference = None
    if 'personalisation' in data:
        personalisation = data['personalisation']
    else:
        personalisation = None
    # Make request to Gov UK Notify API
    response = NOTIFICATIONS_CLIENT.send_email_notification(
        email_address=email,
        template_id=template_id,
        personalisation=personalisation,
        reference=reference,
        email_reply_to_id=None)

    return JsonResponse({"notifyId": response['id'], "message": "Email sent successfully"}, status=201)


def __send_sms_via_notify(data):
    """
    This method actually makes the post request to the Notify endpoint
    :param data: All of the necessary parameters for a successful SMS Notify request are passed in via the request
    :return: The a 201 and the notify id if the request to Notify is successful
    """
    # Read serialized SMS Info
    phone_number = data['phone_number']
    template_id = data['template_id']

    if 'reference' in data:
        reference = data['reference']
    else:
        reference = None
    if 'personalisation' in data:
        personalisation = data['personalisation']
    else:
        personalisation = None
    # Make request to Gov UK Notify API
    response = NOTIFICATIONS_CLIENT.send_sms_notification(
        phone_number=phone_number,
        template_id=template_id,
        personalisation=personalisation,
        reference=reference,
        sms_sender_id=None
    )

    return JsonResponse({"notifyId": response['id'], "message": "SMS sent successfully"}, status=201)


def __format_error(ex):
    """
    This to format errors so that they are human-readable
    :param ex: Serializer exception
    :return: formatted error message
    """
    # Formatting default Django error messages
    err = str(ex).split(":", 1)
    err[0] = err[0].strip('{')
    err[1] = err[1].strip('}')
    err[1] = err[1].replace('[', '')
    err[1] = err[1].replace(']', '')
    return err
