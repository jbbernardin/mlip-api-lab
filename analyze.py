from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
import time
from sec import cred

endpoint = cred['endpoint']
key = cred['key']

credentials = CognitiveServicesCredentials(key)

client = ComputerVisionClient(
    endpoint=endpoint,
    credentials=credentials
)

# Check to see if the computer vision API is working
# domain = "landmarks"
# url = "https://upload.wikimedia.org/wikipedia/commons/4/4d/Cat_March_2010-1.jpg"
# language = "en"
# max_descriptions = 3

# analysis = client.describe_image(url, max_descriptions, language)

# for caption in analysis.captions:
#     print(caption.text)
#     print(caption.confidence)

def read_image(uri):
    numberOfCharsInOperationId = 36
    maxRetries = 10

    # SDK call
    rawHttpResponse = client.read(uri, language="en", raw=True)

    # Get ID from returned headers
    operationLocation = rawHttpResponse.headers["Operation-Location"]
    idLocation = len(operationLocation) - numberOfCharsInOperationId
    operationId = operationLocation[idLocation:]

    # SDK call
    result = client.get_read_result(operationId)
    
    # Try API
    retry = 0
    
    while retry < maxRetries:
        if result.status.lower () not in ['notstarted', 'running']:
            break
        time.sleep(1)
        result = client.get_read_result(operationId)
        
        retry += 1
    
    if retry == maxRetries:
        return "max retries reached"

    if result.status == OperationStatusCodes.succeeded:
        res_text = " ".join([line.text for line in result.analyze_result.read_results[0].lines])
        return res_text
    else:
        return "error"
