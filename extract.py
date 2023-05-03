import requests
from decouple import config

API_KEY = config('API_KEY')



def createDocType(): 
    url = "https://api.sensible.so/v0/document_types"


    payload = {
        "schema": {
            "fingerprint_mode": "fallback_to_all",
            "ocr_engine": "microsoft",
            "prevent_default_merge_lines": True,
            "ocr_level": 2
        },
        "name": "pdf_tables"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


def createConfig():
    url = "https://api.sensible.so/v0/document_types/ID_RETURNED_WHILE_MAKING_DOCU_TYPE/configurations"

    payload = {
        "name": "extract_table",
        "configuration": "{   \"fields\": [     {       \"id\": \"speed_records_table\",       \"anchor\": \"Speed (mph)\",       \"type\": \"table\",       \"method\": {         \"id\": \"fixedTable\",         \"columnCount\": 5,         \"columns\": [           {             \"id\": \"Speed (mph)\",             \"index\": 0           },           {             \"id\": \"Driver\",             \"index\": 1           },           {             \"id\": \"Car\",             \"index\": 2           },           {             \"id\": \"Engine\",             \"index\": 3           },           {             \"id\": \"Date\",             \"index\": 4           },         ],         \"stop\": {           \"type\": \"startsWith\",           \"text\": \"Example 5\"         }       }     },   ] }",
        "publish_as": "production"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

def getUploadUrl():
    url = "https://api.sensible.so/v0/document_types/ID_RETURNED_WHILE_MAKING_DOCU_TYPE/goldens"


    payload = {
        "name": "pdf_with_table",
        "configuration": "extract_table"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


def uploadRefDoc():

    d_name = "relative document path here"

    url = "UPLOAD_URL_HERE"

    headers = {}

    with open(d_name, 'rb') as fp:
        pdf_file = fp.read()
        response = requests.put(url, headers=headers, data=pdf_file)

    print(response)

def extractTable():
    d_name = "relative/document/path/here"
    d_type = "pdf_tables"
    env = "production"
    API_KEY = config('API_KEY')

    url = f"https://api.sensible.so/v0/extract/{d_type}?environment={env}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-type": "application/pdf"
    }

    with open(d_name, 'rb') as fp:
        pdf_file = fp.read()
        response = requests.post(url, headers=headers, data=pdf_file)

    print(f"Extraction Status code: {response.status_code}")

    if response.status_code == 200:
        print(response.json())
    else:
        print(response.json())



def createExcel():

    url = "https://api.sensible.so/v0/generate_excel/EXTRACTION_ID_RECEIVED_IN_STEP_6"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(url, headers=headers)

    print(response.text)



