import requests
import json
import sys, os
from dotenv import load_dotenv

load_dotenv()

SENSIBLE_API_KEY = os.environ["API_KEY"]


def create_document_type(document_type_name):
    url = "https://api.sensible.so/v0/document_types"

    payload = {
        "schema": {
            "fingerprint_mode": "fallback_to_all",
            "ocr_engine": "microsoft",
            "prevent_default_merge_lines": True,
            "ocr_level": 2
        },
        "name": document_type_name
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer {}".format(SENSIBLE_API_KEY)
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("New document type created")
        response_data = response.json()
        return response_data["id"]
    else:
        print("Document type with the name {} already exists. Please choose a different name".format(document_type_name))
        return None


def create_configuration_for_doc_type(document_type_id):
    url = "https://api.sensible.so/v0/document_types/{}/configurations".format(document_type_id)

    payload = {
        "name": "extract_table",
        "configuration": json.dumps({
            "fields": [
                {
                    "id": "speed_records_table",
                    "anchor": "Speed (mph)",
                    "type": "table",
                    "method": {
                        "id": "fixedTable",
                        "columnCount": 5,
                        "startOnRow": 1,
                        "columns": [
                            {
                                "id": "Speed (mph)",
                                "index": 0
                            }, {
                                "id": "Driver",
                                "index": 1
                            }, {
                                "id": "Car",
                                "index": 2
                            }, {
                                "id": "Engine",
                                "index": 3
                            }, {
                                "id": "Date",
                                "index": 4
                            }
                        ],
                        "startOnRow": 1,
                        "stop": {
                            "type": "startsWith",
                            "text": "Example 5"
                        }
                    }
                },
            ]
        }),
        "publish_as": "development"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer {}".format(SENSIBLE_API_KEY)
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("New configuration created")
    else:
        print("Configuration already exists. Use a new name")


def upload_reference_document(document_type_id):

    # Generate upload URL for reference document first
    url = "https://api.sensible.so/v0/document_types/{}/goldens".format(document_type_id)

    payload = {
        "name": "pdf_with_table",
        "configuration": "extract_table"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer {}".format(SENSIBLE_API_KEY)
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        print("Failed to create upload URL for reference document")
        return None

    response_data = json.loads(response.text)
    upload_url = response_data["upload_url"]

    # Upload the reference document to the retrieve upload URL
    reference_document_path = "ref-doc.pdf"
    headers = {}

    with open(reference_document_path, 'rb') as fp:
        pdf_file = fp.read()
        response = requests.put(upload_url, headers=headers, data=pdf_file)

        if response.status_code == 200:
            print("Reference document uploaded")
        else:
            print("Failed to upload reference document")


def extract_table_from_pdf(test_document_path):
    document_type_name = "automobile_land_speed_records"

    url = "https://api.sensible.so/v0/extract/{}?environment=development".format(document_type_name)

    headers = {
        "Authorization": "Bearer {}".format(SENSIBLE_API_KEY),
        "Content-type": "application/pdf"
    }

    with open(test_document_path, 'rb') as fp:
        pdf_file = fp.read()
        response = requests.post(url, headers=headers, data=pdf_file)

    if response.status_code == 200:
        response_data = response.json()

        print("Extraction completed")
        return response_data["id"]
    else:

        print("Extraction failed")
        return None


def convert_extraction_to_excel(extraction_id):
    url = "https://api.sensible.so/v0/generate_excel/{}".format(extraction_id)

    headers = {
        "accept": "application/json",
        "authorization": "Bearer {}".format(SENSIBLE_API_KEY)
    }

    response = requests.get(url, headers=headers)

    print("Conversion completed")
    response_data = response.json()

    if response.status_code == 200:
        return response_data["url"]
    else:
        print("Conversion failed")
        return None


def download_excel_file(file_url):
    response = requests.get(file_url)

    if response.status_code == 200:
        open("result.xlsx", 'wb').write(response.content)
        print("The Excel file has been downloaded at ./result.xlsx")
    else:
        print("The Excel file could not be downloaded")


def setup_sensible():
    document_type_name = "automobile_land_speed_records"
    document_type_id = create_document_type(document_type_name)

    if (document_type_id == None):
        return

    create_configuration_for_doc_type(document_type_id)
    upload_reference_document(document_type_id)


def extract_table_from_pdf_in_excel(test_document_path):
    extraction_id = extract_table_from_pdf(test_document_path)

    if (extraction_id == None):
        return

    xls_file_url = convert_extraction_to_excel(extraction_id)

    if (xls_file_url == None):
        return

    download_excel_file(xls_file_url)


def main():
    arguments = sys.argv

    # Check if "convert" or "setup" is provided as the first argument
    if (len(arguments) < 2 or (arguments[1] != "setup" and arguments[1] != "convert")):
        print('Provide either of "setup" or "convert" as argument')

    # For "setup", run the set up function
    elif (arguments[1] == "setup"):
        print("Setting up Sensible for the first extraction...")
        setup_sensible()

    # For "convert", check if the path to test document is provided and run the extraction function
    elif (arguments[1] == "convert"):

        # if the path of the test document isn't provided as a second argument, exit
        if (len(arguments) < 3):
            print('Provide path to PDF for copying table')
            return

        test_document_path = arguments[2]
        print(
            "Extracting table from {} and converting to Excel...".format(test_document_path))

        extract_table_from_pdf_in_excel(test_document_path)


main()
