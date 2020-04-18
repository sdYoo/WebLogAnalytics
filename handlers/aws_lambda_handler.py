# -*- coding: utf-8 -*-
import json
from utils import *
from zipfile import ZipFile


class LambdaHandler:

    def start_main(self):
        _lambda_client = Utils.get_client(self, "lambda", self._lambda_endpoint_url, self._aws_region)

        _exist_result = Utils.exist_lambda_function(self, _lambda_client)

        if _exist_result:
            print("[Log] Delete lambda function")
            LambdaHandler.delete_lambda_function(self, _lambda_client)

        print("[Log] Create lambda function")
        # 람다 생성
        LambdaHandler.create_lambda_function(self, _lambda_client)
        
        # 람다 조회 InvocationType='Event'|'RequestResponse'|'DryRun'
        res = LambdaHandler.invoke_function_and_get_message(self, _lambda_client, 'DryRun')
        print("[Log] Lambda Info: ", res)

        # register stream consumer
        _rtn_consumer_map = LambdaHandler.connect_datastream_to_lambda(self, _lambda_client)
        print("[Log] consumer status: ", _rtn_consumer_map)

    def create_lambda_function(self, _lambda_client):
        LambdaHandler.create_lambda_zip(self)

        with open(self._lambda_zip_path, 'rb') as f:
            zipped_code = f.read()

        _lambda_client.create_function(
            FunctionName=self._lambda_func_name,
            Runtime='python3.6',
            Role='arn:aws:iam::000000000000:role/adminRole',
            Handler=self._lambda_func_name + '.handler',
            Code=dict(ZipFile=zipped_code)
        )

    def create_lambda_zip(self):
        with ZipFile(self._lambda_zip_path, 'w') as z:
            z.write(self._lambda_func_path + '.py')
            z.close()

    def invoke_function_and_get_message(self, _lambda_client, invo_type):
        _response = _lambda_client.invoke(
                        FunctionName=self._lambda_func_name,
                        InvocationType=invo_type
                    )

        if invo_type == 'RequestResponse':
            _rtn_data=json.loads(_response['Payload'].read().decode('utf-8'))
        else:
            _rtn_data=_response['StatusCode']

        return _rtn_data

    def delete_lambda_function(self, _lambda_client):
        _response = _lambda_client.delete_function(
                        FunctionName=self._lambda_func_name
                    )

        return _response

    def connect_datastream_to_lambda(self, _lambda_client):
        _res_evt_map = LambdaHandler.create_event_mapping(self, _lambda_client)
        return _res_evt_map

    def create_event_mapping(self, _lambda_client):
        _res_evt_map = _lambda_client.create_event_source_mapping(
                            EventSourceArn='arn:aws:kinesis:us-east-1:000000000000:stream/weblog-kinesis-datastream',
                            FunctionName=self._lambda_func_name,
                            BatchSize=500,
                            StartingPosition='AT_TIMESTAMP',
                            StartingPositionTimestamp=1541139109,
                            DestinationConfig={
                                'OnSuccess': {
                                    'Destination': 'OnSuccess'
                                },
                                'OnFailure': {
                                    'Destination': 'OnFailure'
                                }
                            }
                            #MaximumRecordAgeInSeconds=123,
                            #BisectBatchOnFunctionError=True|False,
                            #MaximumRetryAttempts=123
                            # MaximumBatchingWindowInSeconds=123,
                            # ParallelizationFactor=123,
                            # StartingPosition='TRIM_HORIZON'|'LATEST'|'AT_TIMESTAMP',
                            # StartingPositionTimestamp=datetime(2015, 1, 1),
                        )
        print("create_event_mapping() - start ")
        print(_res_evt_map)
        print("create_event_mapping() - stop ")

        return _res_evt_map