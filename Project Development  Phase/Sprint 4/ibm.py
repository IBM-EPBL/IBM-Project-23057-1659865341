import array as arr
import numpy as np
import json

import requests
from json import JSONEncoder


class NumpyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "gQKptWaYIQFpIY14P2Q3FR5mSyWlkwDtcC9ovkqllYdA"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token',
                               data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + mltoken}

values = np.ndarray([0, 0, 3, 1, 647, 56, 11])
print(values.shape)


# NOTE: manually define and pass the array(s) of values to be scored in the next line
# payload_scoring = json.dumps({"input_data": [{"fields": [['homepage_featured', 'emailer_for_promotion', 'op_area', 'cuisine', 'city_code', 'region_code', 'category']], "values": [[0, 0, 3, 1, 647, 56, 11], [1, 1, 2, 3, 600, 46, 19]]}]}, cls=NumpyEncoder)

payload_scoring = {"input_data": [{"field": [['homepage_featured', 'emailer_for_promotion', 'op_area', 'cuisine',
                                              'city_code', 'region_code', 'category']], "values": [[0, 0, 3, 1, 647, 56, 11], [1, 1, 2, 3, 600, 46, 19]]}]}

print(type(payload_scoring['input_data'][0]))

response_scoring = requests.post(
    'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/07706ceb-d908-4138-b5f8-a649a9ad3f07/predictions?version=2022-11-24',
    json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})


print("Scoring response")
predictions = response_scoring.json()
for i in predictions:
    print(i, predictions[i])
