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