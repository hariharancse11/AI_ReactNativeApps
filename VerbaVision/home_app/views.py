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

    from_email = 'hariharan.sekar@ionidea.com'#request.data.get('from_email')
    to_email = request.data.get('to_email')
    otp = str(random.randint(100000, 999999))  # Generate a random 6-digit OTP

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key[
        'api-key'] = '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'

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = "CRM App Password Reset"
    # html_content = f"<html><body><h3>OTP Verification<br>Your OTP is: {otp} </h3></body></html>"
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CRM App Password Reset</title>
</head>
<body>
    <h2>CRM App Password Reset</h2>
    <p>Dear User,</p>
    <p>We received a request to reset your password for the CRM App. To proceed with the password reset, please use the following One-Time Password (OTP):</p>
    <p style="font-weight: bold; font-size: 18px;">{ otp }</p>
    <p>If you did not request this password reset, please ignore this email and contact our support team.</p>
    <p>Thank you,</p>
    <p>The CRM App Team</p>
</body>
</html>
"""
    sender = {"name": from_email, "email": from_email}
    to = [{"email": to_email, "name": to_email}]
    # cc = [{"email": "example2@example2.com", "name": "Janice Doe"}]
    # bcc = [{"name": "John Doe", "email": "example@example.com"}]
    # reply_to = {"email": "replyto@domain.com", "name": "John Doe"}
    headers = {"Password Reset": "CRM App password reset"}
    # params = {"parameter": "My param value", "subject": "New Subject"}
    # send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, bcc=bcc, cc=cc, reply_to=reply_to, headers=headers,html_content=html_content, sender=sender, subject=subject)
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers,
                                                   html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        request.session['otp'] = otp
        # print(request.session['otp'])
        return Response({
            'Status': True,
            'Msg': 'OTP sent successfully',
            'Data': None
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