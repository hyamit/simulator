from zeep import Client
from zeep.exceptions import Fault
from zeep.wsse.username import UsernameToken

# Define the SOAP endpoint URL for the Calculator service
soap_url = "http://www.dneonline.com/calculator.asmx?wsdl"

# Maximum number of retries
max_retries = 3

def perform_addition(int_a, int_b):
    # Retry logic
    for retry in range(max_retries):
        try:
            # Create a Zeep client
            client = Client(soap_url)

            # Add WS-Security UsernameToken (if required by the service)
            # client.wsse.set_password('username', 'password')

            # Call the Add operation
            result = client.service.Add(intA=int_a, intB=int_b)

            # Print the result of addition
            print(f"Result of adding {int_a} and {int_b}: {result}")

            # Break out of the retry loop if successful
            break

        except Fault as e:
            print(f"Error from SOAP service (Attempt {retry + 1}/{max_retries}): {e.message}")

        except Exception as e:
            print(f"Error connecting to the SOAP service (Attempt {retry + 1}/{max_retries}): {e}")

# Example: Perform addition of 5 and 10
perform_addition(5, 10)
