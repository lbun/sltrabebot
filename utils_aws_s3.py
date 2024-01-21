import boto3
import json
import pandas as pd
import time
import datetime


class AwsClient:
    def __init__(self):
        self.bucket_name = "tradebot24"
        self.s3client = boto3.client('s3')
        self.last_transaction_object = 'last_transaction.json'
        self.daily_transactions_object = f"trades/{datetime.datetime.now().strftime('%Y%m%d')}.json"
        self.portfolio_value_object = f"portfolio/time_value.json"
    
    def list_files_folder(self, prefix_folder="trades"):
        try:
            # List objects in the specified folder
            response = self.s3client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix_folder)
            # Extract file keys from the response
            files = [obj['Key'] for obj in response.get('Contents', [])]
            return files
        except Exception as e:
            print(f"Error listing files in folder: {e}")
            return []
        
    def load_portfolio_values(self):
        try:
            object_key_path = self.portfolio_value_object
            response = self.s3client.get_object(Bucket=self.bucket_name, Key=object_key_path)
            json_content = response['Body'].read().decode('utf-8')
            portfolio_values = json.loads(json_content)
        except Exception as e:
            if "The specified key does not exist." in e.args[0]:
                portfolio_values = []
        finally:
            return portfolio_values
    
   
    def load_daily_transactions_list(self):
        """
        Load the daily transaction list from s3 and return it. 
        In case on no file, returns an empty list
        """
        try:
            object_key_path = self.daily_transactions_object
            response = self.s3client.get_object(Bucket=self.bucket_name, Key=object_key_path)
            # Read and parse the JSON content
            json_content = response['Body'].read().decode('utf-8')
            transactions = json.loads(json_content)
            # Now, `data` contains the parsed JSON content
            return transactions
        except Exception as e:
            if "The specified key does not exist." in e.args[0]:
                data = json.dumps([])
                self.s3client.put_object(Bucket=self.bucket_name, Key=object_key_path, Body=data)
                return []
            else:
                print(f'Error: {e}')

if __name__=="__main__":
    portfolio_values = AwsClient().last_transaction_object()
    print("finished")