from django.http import HttpResponse, JsonResponse
from notifications_python_client.errors import HTTPError
from notifications_python_client.notifications import NotificationsAPIClient
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from application.serializers import EmailSerializer, SmsSerializer, NotifySerializer
from django.conf import settings
import logging
import traceback 

log = logging.getLogger('django.server')
NOTIFICATIONS_CLIENT = NotificationsAPIClient(settings.NOTIFY_API_KEY)

@api_view(['PUT'])
def change_api_key(request):
    #This method is for updating the API key
    try:
        serializer = NotifySerializer(data=request.data)
        if serializer.is_valid():
            #API key set
            NOTIFICATIONS_CLIENT = NotificationsAPIClient(serializer.data['apiKey'])
            return JsonResponse({"message":"Api key successfully updated"}, status=200)
        err = formatError(serializer.errors)
        log.error("Django serialization error: " +err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error":"Bad Request",}, status=status.HTTP_400_BAD_REQUEST)
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
def send_email(request):
    #This method handles the send Email requests and responses
    try:
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            #call method to send email
            return send_email_via_notify(serializer.data)
        err = formatError(serializer.errors)
        log.error("Django serialization error: " +err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
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
    #This method handles the send SMS request and responses
    try:
        serializer = SmsSerializer(data=request.data)
        if serializer.is_valid():
            return send_sms_via_notify(serializer.data)
        err = formatError(serializer.errors)
        log.error("Django serialization error: " +err[0] + err[1])
        return JsonResponse({"message": err[0] + err[1], "error":"Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
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


def send_email_via_notify(data):
    #Read serialized email info
    email = data['email']
    template_id = data['templateId']    
    if 'reference' in data:
        reference = data['reference']
    else:
        reference = None
    if 'personalisation' in data:
        personalisation = data['personalisation']
    else:
        personalisation = None
    #Make request to Gov UK Notify API
    response = NOTIFICATIONS_CLIENT.send_email_notification(
        email_address=email,
        template_id=template_id,
        personalisation=personalisation,
        reference=reference,
        email_reply_to_id=None)

    return JsonResponse({"notifyId": response['id'], "message":"Email sent successfully"}, status=201)


def send_sms_via_notify(data):
    #Read serialized SMS Info
    phone_number = data['phoneNumber']
    template_id = data['templateId']

    if 'reference' in data:
        reference = data['reference']
    else:
        reference = None
    if 'personalisation' in data:
        personalisation = data['personalisation']
    else:
        personalisation = None
    #Make request to Gov UK Notify API
    response = NOTIFICATIONS_CLIENT.send_sms_notification(
        phone_number=phone_number,
        template_id=template_id,
        personalisation=personalisation,
        reference=reference,
        sms_sender_id=None
    )

    return JsonResponse({"notifyId": response['id'],"message":"SMS sent successfully"}, status=201)
def formatError(ex):
    #Formatting default Django error messages
    err = str(ex).split(":",1)
    err[0] = err[0].strip('{')
    err[1] = err[1].strip('}')
    err[1] = err[1].replace('[','')
    err[1] = err[1].replace(']','')
    return err