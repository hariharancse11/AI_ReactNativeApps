from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
# Create your views here.
from rest_framework.decorators import api_view
from transformers import pipeline

@api_view(['GET'])
def home(request):
    return Response('you made it!')


@api_view(['GET'])
def generate_text(request):
    # Create the text generation pipeline
    generator = pipeline("text-generation", model="distilgpt2")

    # Generate text
    input_prompt = request.GET.get('text')
    no_of_words = request.GET.get('no_of_words')
    print(input_prompt,no_of_words)
    generated_text = generator(input_prompt, max_length=int(no_of_words), num_return_sequences=1)

    # Print the generated text
    res = generated_text[0]['generated_text'].replace('\n','')
    #print(res)

    return Response(res)

import time
import pyotp
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail
import random
import sib_api_v3_sdk
SECRET_KEY = ''
def generate_secretkey():
    return pyotp.random_base32()

@api_view(['POST'])
def send_otp(request):
    generate_secretkey()

    # Generate TOTP based on the secret key
    totp = pyotp.TOTP(SECRET_KEY)
    otp = totp.now()
    from_email = 'hariharan.sekar@ionidea.com'  # request.data.get('from_email')
    to_email = request.data.get('to_email')
    print(otp)

    try:
        return Response({
            'Status': True,
            'Msg': 'OTP sent successfully',
            'Data': None
        })

    except Exception as e:
        return Response({
            'Status': False,
            'Msg': f'Failed to send email: {str(e)}',
            'Data': None
        })

@api_view(['POST'])
def validate_otp(request):
    # Generate TOTP based on the secret key
    totp = pyotp.TOTP(SECRET_KEY)

    # Get the current time on the server
    current_time = int(time.time())

    # Define the time step and tolerance (30 seconds in this example)
    time_step = 30
    tolerance = 1

    # Generate OTPs for the current time and within the tolerance window
    otp_generated = []
    for i in range(-tolerance, tolerance + 1):
        otp_generated.append(totp.at(current_time + i * time_step))
    # Validate the OTP entered by the user
    try:
        otp = str(request.data.get('otp'))
        email = str(request.data.get('email'))
        new_password = str(request.data.get('new_password'))
        #print(otp, totp.now())

        if otp in otp_generated:
            # Correct OTP
            # if serializer.is_valid():
            #     user = User.objects.get(email=serializer.validated_data['email'])
            #     serializer.validated_data['password'] = hashed_password
            #     serializer.update(user, serializer.validated_data)

            return Response({
                'Status': True,
                'Msg': f'Password reset successful',
                'Data': None
            })

        else:
            # Incorrect OTP or missing OTP
            return Response({
                'Status': False,
                'Msg': f'{otp} is Invalid',
                'Data': None
            })
    except Exception as e:
        return Response({
            'Status': False,
            'Msg': f'Error: Something went wrong '+str(e),
            'Data': None
        })