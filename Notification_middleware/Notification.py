import pymysql
import os
import random
import boto3
import json

class SNS_Notification:

    def __int__(self):
        pass

    @staticmethod
    def get_connection_sns():
        key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        sns_client = boto3.client('sns', region_name='us-east-1', aws_access_key_id=key_id, aws_secret_access_key=key)
        return sns_client

    @staticmethod
    def publish_notification( message, dic_attribute):
        client = SNS_Notification.get_connection_sns()
        res = client.publish(
            TopicArn = 'arn:aws:sns:us-east-1:056111268658:Sevenlearner_SNS',
            Message = message,
            MessageAttributes=dic_attribute
        )

        return True

    @staticmethod
    def send_email_notification(accountInfor, action):
        Email = accountInfor['Email']
        Name = accountInfor['FirstName'] + " " + accountInfor['LastName']
        if action == "create":

            message = f'Dear {Name}, \n \n Your have sucessfully create your sevenlearnerAPP account! Welcome to our APP! \n \n Sincerely,\n Sevenlearner Service team '
        else:
            message = f'Dear {Name}, \n \n Your account information have been updated! \n \n Sincerely,\n Sevenlearner Service team '

        dic_attribute = {}
        dic_attribute['Email'] = {'DataType': 'String', 'StringValue': Email}

        SNS_Notification.publish_notification(message, dic_attribute)

        return True

