import requests

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
    },
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer YOUR_API_KEY"
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
        "authorization": "Bearer YOUR_API_KEY"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)

def uploadRefDoc():

    url = "https://api.sensible.so/v0/document_types/ID_RETURNED_WHILE_MAKING_DOCU_TYPE/goldens"

    payload = {
        "name": "pdf_with_table",
        "configuration": "extract_table"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer YOUR_API_KEY"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


def createExcel():

    url = "https://api.sensible.so/v0/generate_excel/EXTRACTION_ID_RECEIVED_IN_STEP_6"

    headers = {
        "accept": "application/json",
        "authorization": "Bearer YOUR_API_KEY"
    }

    response = requests.get(url, headers=headers)

    print(response.text)

