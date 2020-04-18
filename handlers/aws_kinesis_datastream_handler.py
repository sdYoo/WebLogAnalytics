# -*- coding: utf-8 -*-
import time
from .aws_kinesis_firehose_handler import *
from .aws_s3_handler import *
from utils import *
from botocore.exceptions import ClientError
import json


class KinesisDataStreamHandler():

    def start_main(self):
        _datastream_client = Utils.get_client(self, "kinesis", self._data_stream_endpoint_url, self._aws_region)

        try:
            KinesisDataStreamHandler.create_datastream(self, _datastream_client)
        except ClientError as error_message:
            if error_message.response['Error']['Code'] == 'ResourceInUseException':
                print("kinesis datastream already exists")
            else:
                print("Unexpected error: %s" % error_message)

        # Check to kinesis status active
        while KinesisDataStreamHandler.get_status(self, _datastream_client, 1) != 'ACTIVE':
            time.sleep(1)
        print("stream {} is active".format(self._data_stream_name))

        # Register Consumer
        _reg_consumer = KinesisDataStreamHandler.register_data_stream_consumer(self, _datastream_client)
        print("consumer is registed: ", _reg_consumer)

    def create_datastream(self, client):
        return client.create_stream(
            StreamName=self._data_stream_name,
            ShardCount=1
        )

    def get_status(self, datastream_client, num):
        datastream_response = datastream_client.describe_stream(
                                StreamName=self._data_stream_name,
                                Limit=100,
                                ExclusiveStartShardId='shardId-000000000000'
                            )

        ds_description = datastream_response.get('StreamDescription')
        ds_status = ds_description.get('StreamStatus')
        ds_arn = ds_description.get('StreamARN')

        if num == 1:
            _rtn_status = ds_status
        elif num == 2:
            _rtn_status = ds_arn

        return _rtn_status

    def register_data_stream_consumer(self, _datastream_client):
        _res_data_stream_arn = KinesisDataStreamHandler.get_status(self, _datastream_client, 2)
        print("_res_data_stream_arn: ", _res_data_stream_arn)

        _res_consumer = _datastream_client.register_stream_consumer(
                        StreamARN=_res_data_stream_arn,
                        ConsumerName=self._consumer_name
                        )

        _consumer_info = _res_consumer.get("Consumer")
        _consumer_status = _consumer_info.get("ConsumerStatus")

        return _consumer_status

    def delete_stream_consumer(self, _datastream_client):
        _res_data_stream_arn = KinesisDataStreamHandler.get_status(self, _datastream_client, 2)

        _response = _datastream_client.deregister_stream_consumer(
                        StreamARN=_res_data_stream_arn,
                        ConsumerName=self._consumer_name,
                        ConsumerARN='string'
                    )

        return _response

    def put_log(self):
        print("[Log-put] put_log Start!")
        # Kinesis Put Stream - 1분동안 kinesis datastream에 put 함
        datastream_client = Utils.get_client(self, "kinesis", self._data_stream_endpoint_url, self._aws_region)

        print("[TIME] ", Utils.get_now_timestamp(self))
        dt_timestamp = Utils.get_now_timestamp(self)

        log_file = open("C:\\test\\nginx-1.16.1\\logs\\access.log",'r')
        file_lines = log_file.readlines()
        lines_cnt = 0
        array_records = []

        for file_line in file_lines:
            lines_cnt += 1
            # print("[Log-put] put line >> ", file_line)
            append_record_json = {
                'Data': json.dumps(file_line),
                'PartitionKey': dt_timestamp
            }

            array_records.append(append_record_json)

            log_file.close()

        datastream_client.put_records(
            StreamName=self._data_stream_name,
            Records=array_records
        )
        print("[Log-put] put_log complete!")

    def get_log(self):
        print("[Log-get] get_log Start!")

        log_list = []
        prev_part_key = ""
        n_row_cnt = 0

        list_Shard_Iter_Type =  ['AT_SEQUENCE_NUMBER',
                                 'AFTER_SEQUENCE_NUMBER',
                                 'TRIM_HORIZON',
                                 'LATEST',
                                 'AT_TIMESTAMP']

        print(list_Shard_Iter_Type[3])

        datastream_client = Utils.get_client(self, "kinesis", self._data_stream_endpoint_url, self._aws_region)

        shard_iterator = datastream_client.get_shard_iterator(
                            StreamName=self._data_stream_name,
                            ShardId="shardId-000000000000",
                            ShardIteratorType=list_Shard_Iter_Type[3] # LATEST
                        )

        next_iterator = shard_iterator['ShardIterator']

        while True:
            shard_iterator = datastream_client.get_records(
                                ShardIterator=next_iterator,
                                Limit=1
                            )

            part_key = ""

            for dic_data in shard_iterator['Records']:
                part_key = dic_data['PartitionKey']

                if part_key and n_row_cnt == 0:
                    prev_part_key = part_key

                sub_log_json = Utils.convert_log_to_json(dic_data['Data'])
                sub_log_json = json.dumps(sub_log_json)

                # print("[Log-get] sub_log_json: ", sub_log_json)
                log_list.append(sub_log_json)
                n_row_cnt = n_row_cnt+1

            next_iterator = shard_iterator['NextShardIterator']
            time.sleep(0.5)

            # print("prev_part_key: ", prev_part_key)
            # print("part_key: ", part_key)
            if not part_key:
                print("[Log-get] sub_log_json: ", log_list)
                break

        main_log_json = OrderedDict()
        main_log_json["name"] = "awslog{}".format(prev_part_key)
        main_log_json["logs"] = log_list

        print(json.dumps(main_log_json, indent=4, ensure_ascii=False))
        print("[Log-get] get_log complete!")

        # Kinesis Firehose S3 Upload
        _firehose_client = Utils.get_client(self, "firehose", self._firehose_endpoint_url, self._aws_region)
        _res_put_firehose = KinesisFirehoseHandler.put_record_to_delivery_stream(self, _firehose_client, main_log_json)

        print("[Log] FireHose Completed: ", _res_put_firehose)

        _list_bucket_obj = S3Handler.select_s3_bucket_objs(self)
        print("[Log-S3] ", _list_bucket_obj)

        S3Handler.select_s3_file(self)

        return main_log_json

