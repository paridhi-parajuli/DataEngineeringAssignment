"""

Program to mask PII data.
Author: Paridhi Parajuli
Date created: 2023/02/1

"""
import boto3
import psycopg2
import json
import base64

#Declaring variables needed for connection. Users need to set these variables before executing the program.
USERNAME = "postgres"
PASSWORD = "postgres"
HOST = "httsp://localhost:5432"
DB = "postgres"
ENDPOINT_URL = " http://localhost:4566/000000000000"
QUEUE_NAME = "login-queue"


def encoder(message,is_encode):
    """This functions does encoding and decoding of messages
    Arguments:
            message: str
            is_encode: Boolean
    Returns:
            transformed message
    
    """
    if is_encode:
        new_message = base64.b64encode(message.encode('ascii')).decode('utf-8')
    else:
        new_message = base64.b64decode(message).decode('utf-8')
    return new_message


def post_data(message):
    """This function is used to post the transformed data to postgres database"""
    connection  = psycopg2.connect(
            host =  encoder(HOST, False),
            database = encoder(DB,False),
            user =  encoder(USERNAME,False),
            password = encoder(PASSWORD,False)
        )
    con_obj = connection.cursor()
    con_obj.execute("""CREATE TABLE IF NOT EXISTS user_logins(
                        user_id varchar(128),
                        device_type varchar(32),
                        masked_ip varchar(256),
                        masked_device_id varchar(256),
                        locale varchar(32),
                        app_version integer,
                        create_date date
                        );""")
    connection.commit()
    for i in message:
        con_obj.execute("""INSERT INTO user_logins ( user_id, app_version, 
                device_type, masked_ip, locale, masked_device_id, create_date \
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)""", list(i.values()))
        connection.commit()
    connection.close()
    return


def main():
    """This is the main module where the execution starts"""

    # Reading data from the queue
    client = boto3.client("sqs", endpoint_url = ENDPOINT_URL)
    response = client.receive_message(
        QueueUrl= ENDPOINT_URL + '/' + QUEUE_NAME,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=25
    )
    new_message = []
    for message in response['Messages']:
        data = json.loads(message['Body'])
        ip = data['ip']
        device_id = data['device_id']

        en_ip= encoder(data['ip'],True)
        en_device= encoder(data['device_id'],True)

        data['ip'] = en_ip
        data['device_id'] = en_device
        new_message.append(data)
    post_data(new_message)
    return 

if __name__ == "__main__":
    main()