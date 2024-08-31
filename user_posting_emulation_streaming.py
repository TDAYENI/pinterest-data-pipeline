import requests
import random
from time import sleep
import json
import sqlalchemy
from sqlalchemy import text
import yaml

random.seed(100)

# Load DB credentials
with open('cred/db_creds.yaml', 'r') as f:
    db_cred = yaml.load(f, Loader=yaml.SafeLoader)


class AWSDBConnector:
    """
    Class for connecting to the AWS RDS database.
    """

    def __init__(self):
        self.HOST = db_cred['HOST']
        self.USER = db_cred['USER']
        self.PASSWORD = db_cred['PASSWORD']
        self.DATABASE = db_cred['DATABASE']
        self.PORT = 3306

    def create_db_connector(self):
        engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine


# Kinesis URLs for invoking API
pin_stream_name = "streaming-0e2685691ff5-pin"
geo_stream_name = "streaming-0e2685691ff5-geo"
user_stream_name = "streaming-0e2685691ff5-user"

pin_invoke_url = f"https://pzp2pscs5m.execute-api.us-east-1.amazonaws.com/v1/streams/{pin_stream_name}/record"
geo_invoke_url = f"https://pzp2pscs5m.execute-api.us-east-1.amazonaws.com/v1/streams/{geo_stream_name}/record"
user_invoke_url = f"https://pzp2pscs5m.execute-api.us-east-1.amazonaws.com/v1/streams/{user_stream_name}/record"

headers = {'Content-Type': 'application/json'}

# Function to send data to Kinesis streams via the API


def send_data_to_kinesis(data, stream_name, invoke_url):
    payload = json.dumps({
        "StreamName": stream_name,
        "Data": data,
        "PartitionKey": "index" if stream_name == pin_stream_name else "ind"
    })

    try:
        response = requests.put(invoke_url, headers=headers, data=payload)
        response.raise_for_status()
        print(f"Sent data to {stream_name}: Status Code: {
              response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to Kinesis: {e}")


def run_infinite_post_data_loop():
    """
    Infinitely runs the process of fetching random data from database tables
    and posting it to corresponding AWS Kinesis streams.
    """
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:
            # Fetch random rows from database tables
            pin_string = text(
                f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            for row in pin_selected_row:
                pin_result = dict(row._mapping)
                send_data_to_kinesis(
                    pin_result, pin_stream_name, pin_invoke_url)

            geo_string = text(
                f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            for row in geo_selected_row:
                geo_result = dict(row._mapping)
                geo_result['timestamp'] = geo_result['timestamp'].isoformat()
                send_data_to_kinesis(
                    geo_result, geo_stream_name, geo_invoke_url)

            user_string = text(
                f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            for row in user_selected_row:
                user_result = dict(row._mapping)
                user_result['date_joined'] = user_result['date_joined'].isoformat()
                send_data_to_kinesis(
                    user_result, user_stream_name, user_invoke_url)

            print("Sent data to Kinesis streams.")


if __name__ == "__main__":
    new_connector = AWSDBConnector()
    run_infinite_post_data_loop()
    print('Working')
