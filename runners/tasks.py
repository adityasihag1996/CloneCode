import time

def process_data(json_data):
    print("Received JSON data:", json_data)
    exec(json_data["code"])
    time.sleep(1)