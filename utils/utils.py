# -*- coding: utf-8 -*-
import argparse
import re
import shutil
import datetime
import boto3
import os
import requests

from collections import OrderedDict
from botocore.errorfactory import ClientError


class Utils:

    def start_main(self):
        print("[Log-Start] Utils Start")
        # 0. connect to localstack
        Utils.check_conn_localstack(self)
        # 1. create Util
        Utils.help_command(self)
        # create lambda path - 람다 파일 C드라이브 하위로 복사
        Utils.copy_lambda_function(self)

    def get_client(self, aws_service, endpoint_url, region_name):
        _aws_service_client = boto3.client(aws_service,
                          endpoint_url=endpoint_url,
                          use_ssl=False,
                          aws_access_key_id="",
                          aws_secret_access_key="",
                          region_name=region_name)

        return _aws_service_client

    def exist_s3_bucket(s3_client, bucket_name):
        result = ""
        try:
            result = s3_client.list_objects(Bucket=bucket_name)
        except ClientError as error_message:
            print("[ErrorLog]", error_message)
            exists = False
            pass

        if result:
            exists = True

        return exists

    def exist_lambda_function(self, lambda_client):
        print("Lambda_Function_is_exist_Check()")
        try:
            lambda_client.get_function(
                        FunctionName=self._lambda_func_name
                        # Qualifier='string'
            )
            exists = True
        except ClientError as error_message:
            print("[ErrorLog]", error_message)
            exists = False
            pass

        return exists

    def exist_kinesis_firehose(firehose_client, firehose_name):
        print("kinesis_firehose_is_exist()")
        try:
            result = firehose_client.list_delivery_streams(
                DeliveryStreamType="KinesisStreamAsSource",
                ExclusiveStartDeliveryStreamName=firehose_name
            )
        except ClientError as error_message:
            print("[ErrorLog]", error_message)
            exists = False
            pass

        if result:
            exists = True

        return exists

    def convert_log_to_json(str_log_line):
        # Ready for json data
        str_log_line = str_log_line.decode()
        str_log_line = str_log_line.replace('\\n"', '')
        str_log_line = str_log_line.replace('\\', '')

        # regular expression
        regex_host = r'\"(?P<host>.*?)'
        regex_space = r'\s'
        regex_identity = r'(?P<identity>.*)'
        regex_user = r'(?P<user>\S+)'
        regex_time = r'(?P<time>\[.*?\])'
        regex_request = r'\"(?P<request>.*?)\"'
        regex_status = r'(?P<status>\d{3})'
        regex_size = r'(?P<size>\S+)'
        regex_refer = r'\"(?P<referrer>.*?)\"'
        regex_user_agent = r'\"(?P<user_agent>.+)\"'

        regex =  regex_host + regex_space + regex_identity + regex_space + regex_user + regex_space + regex_time + regex_space + regex_request + regex_space
        regex += regex_status + regex_space + regex_size + regex_space + regex_refer + regex_space + regex_user_agent

        match_data = re.search(regex, str_log_line)

        sub_log_json = OrderedDict()
        sub_log_json["host"] = match_data.group('host')
        sub_log_json["time"] = match_data.group('time')
        sub_log_json["request"] = match_data.group('request')
        sub_log_json["status"] = match_data.group('status')
        sub_log_json["size"] = match_data.group('size')
        sub_log_json["referrer"] = match_data.group('referrer')
        sub_log_json["user_agent"] = match_data.group('user_agent')

        return sub_log_json

    def copy_lambda_function(self):
        cp_src_path = self._copy_source_path
        cp_des_path = self._copy_destination_path

        try:
            rtn_message = shutil.copyfile(cp_src_path, cp_des_path)
            print("[Log] Copy File Complete:", rtn_message)
        except Exception as error_message:
            print("[Log] Copy File Error:", error_message)

    def get_now_timestamp(self):
        _dt_timestamp = datetime.datetime.now()
        _dt_timestamp = _dt_timestamp.strftime('%Y%m%d%H%M%S')
        return _dt_timestamp

    def get_file_size(self, src_file):
        src_file_stat = os.stat(src_file)
        print("[Log] src_file_stat :", src_file_stat)

        src_file_size = src_file_stat.st_size
        print("[Log] src_file_size :", src_file_size)

    def check_conn_localstack(self):
        print("[Log-Start] Utils localstack ip :", self._localstack_ip)
        try:
            _res = requests.post(self._localstack_ip, timeout=5)
            # _http_code = _res.status_code
            # print("http_code: ", _http_code)
        except Exception as error_message:
            print("[ErrorLog]", "LocalStack Connect Error : ip {}".format(self._localstack_ip))
            print(error_message)
            pass

    def help_command(self):
        # common arguments
        _parser = argparse.ArgumentParser(prog='ncb', description='''weblogAnalytics version 0.0.1''')
        _parser.add_argument('--conf', '-c', metavar='weblog.json', help='configuration file', required=True)
        _parser.add_subparsers(help='commands')
