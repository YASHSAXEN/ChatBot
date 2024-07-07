from django.shortcuts import render
from django.http import JsonResponse
import json
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

# Function to extract contact details from resume content
def answer_fn(content, question):
    prompt_data = """ 
    Your task is to go understand the information in the {content} and give appropriate answers to given question
    {question}. If the answer is not found then display the Sorry message.
    """
    # Concatenate the transcription with the prompt_data
    prompt = "[INST]" + prompt_data + content + question + "[/INST]"

    s3_session = boto3.Session(aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                            region_name='us-east-1')

    bedrock = s3_session.client(service_name="bedrock-runtime")
    payload = {
        "prompt": prompt,
        "temperature": 0.5,
        "top_p": 0.9
    }
    body = json.dumps(payload)
    model_id = "mistral.mixtral-8x7b-instruct-v0:1"
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(response.get("body").read())
    return response_body['outputs'][0]['text']

def read_json_content(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def read_pdf_content(question):
    # Read JSON content
    json_data = read_json_content("extracted_information.json")
    
    # Extract paragraphs, list_items, tabindex_paragraphs, and pdf_urls from JSON data
    content = ""
    for item in json_data:
        for key, value in item.items():
            if 'paragraphs' in value:
                content += " ".join(value['paragraphs']) + " "
            if 'list_items' in value:
                content += " ".join(value['list_items']) + " "
            if 'tabindex_paragraphs' in value:
                content += " ".join(value['tabindex_paragraphs']) + " "
            if 'pdf_urls' in value:
                content += " ".join(value['pdf_urls']) + " "
    # print(content)
    answer = answer_fn(content, question)

    return answer

    # print("Answer is ", answer)

# Create your views here.
def home(request):
    return render(request,'index.html')

def botresult(request,value):
    if request.method == 'POST':
        result = read_pdf_content(value)
        return JsonResponse({'response':result})
    return JsonResponse({'error':'Invalid request'}, status = 400)
