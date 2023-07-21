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


import random
import sib_api_v3_sdk

@api_view(['POST'])
def send_otp(request):

    
    otp = str(random.randint(100000, 999999))  # Generate a random 6-digit OTP

    
    try:
        request.session['otp'] = otp
        # print(request.session['otp'])
        return Response({
            'Status': True,
            'Msg': 'OTP sent successfully',
            'Data': otp
        })

    except Exception as e:
        return Response({
        'Status': True,
        'Msg': f'Failed to send email: {str(e)}',
        'Data': None
    })


@api_view(['POST'])
def validate_otp(request):
    try:
        otp = str(request.data.get('otp'))
        email = str(request.data.get('email'))
        new_password = str(request.data.get('new_password'))
        stored_otp = str(request.session.get('otp'))
        #print(otp,stored_otp)
        if otp and stored_otp and otp == stored_otp:
            # Correct OTP
            # if serializer.is_valid():
            #     user = User.objects.get(email=serializer.validated_data['email'])
            #     serializer.validated_data['password'] = hashed_password
            #     serializer.update(user, serializer.validated_data)

            del request.session['otp']  # Remove the OTP from the session
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