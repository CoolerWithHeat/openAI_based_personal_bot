import json, base64
import os

def ParseData(action='retrieve', data_to_save = None):
    
    if action == "retrieve":
        with open('developerBackground.txt', 'r') as encoded_file:
            encoded_data = encoded_file.read()
            decoded_data = base64.b64decode(encoded_data)
            json_data = decoded_data.decode()
            return json.loads(json_data)

    elif action == "save":
        if data_to_save:
            json_data = json.dumps(data_to_save)
            encoded_data = base64.b64encode(json_data.encode()).decode()

            with open('developerBackground.txt', 'w') as json_file:
                json_file.write(encoded_data)
                return data_to_save