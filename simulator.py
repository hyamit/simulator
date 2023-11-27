import requests
from requests.exceptions import RequestException
from xml.etree import ElementTree as ET

# Define the SOAP endpoint URL for the Calculator service
soap_url = "http://www.dneonline.com/calculator.asmx"

# SOAP request template for Add operation
soap_request_template = """<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <web:Add>
         <!--Optional:-->
         <web:intA>{int_a}</web:intA>
         <!--Optional:-->
         <web:intB>{int_b}</web:intB>
      </web:Add>
   </soapenv:Body>
</soapenv:Envelope>
"""

# Maximum number of retries
max_retries = 3

def perform_addition(int_a, int_b):
    # Retry logic
    for retry in range(max_retries):
        try:
            # Build SOAP request with parameters
            soap_request = soap_request_template.format(int_a=int_a, int_b=int_b)

            # Define headers for SOAP request
            headers = {
                'Content-Type': 'text/xml',
                'SOAPAction': 'http://tempuri.org/Add',
            }

            # Send SOAP request using requests library
            response = requests.post(soap_url, data=soap_request, headers=headers, timeout=10)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the XML response
                root = ET.fromstring(response.content)
                # Find any child node with text content (handles different response structures)
                result_node = next((child for child in root.iter() if child.text is not None), None)

                if result_node is not None:
                    result = result_node.text
                    # Print the result of addition
                    print(f"Result of adding {int_a} and {int_b}: {result}")
                else:
                    print("Error: Unable to extract result from SOAP response")

                # Break out of the retry loop if successful
                break

            else:
                print(f"Error: HTTP Status Code {response.status_code}")
                # Retry if the status code is not 200

        except RequestException as e:
            print(f"Error connecting to the SOAP service (Attempt {retry + 1}/{max_retries}): {e}")

# Example: Perform addition of 5 and 10
perform_addition(5, 10)
