from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import os

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)

client = PayPalHttpClient(environment)

@api_view(['POST'])
def Paypal(request):
    try:
        datos = request.data
        requerimiento = OrdersCreateRequest()
        requerimiento.prefer('return=representation')
        requerimiento.request_body({
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": "USD",
                            "value": datos["amount"]  # Get amount from request data
                        }
                    }
                ]
            })
        responde = client.execute(requerimiento)
        return Response({'id':f'{responde.result.id}'}, status=status.HTTP_200_OK)
    except:
        return Response({'Error':'fallo'}, status=status.HTTP_400_BAD_REQUEST)