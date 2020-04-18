# -*- coding: utf-8 -*-
from utils import *


class S3Handler:

    def start_main(self):
        print("[Log-Start] S3 Start")
        _s3_client = Utils.get_client(self, "s3", self._s3_endpoint_url, self._aws_region)

        _exist_result = Utils.exist_s3_bucket(_s3_client, self._s3_bucket_name)

        if not _exist_result:
            print("[Log-Start] Bucket is not exists")
            S3Handler.create_s3_bucket(self, _s3_client)

    def create_s3_bucket(self, _s3_client):
        _s3_client.create_bucket(
            Bucket=self._bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': self._aws_region
            }
        )

    def select_s3_bucket_objs(self):
        _s3_client = Utils.get_client(self, "s3", self._s3_endpoint_url, self._aws_region)
        _list_bucket_obj = _s3_client.list_objects(Bucket=self._s3_bucket_name)

        return _list_bucket_obj

    def select_s3_file(self):
        _s3_client = Utils.get_client(self, "s3", self._s3_endpoint_url, self._aws_region)
        _paginator = _s3_client.get_paginator('list_objects')
        _page_iterator = _paginator.paginate(Bucket=self._s3_bucket_name)

        n_num = 0

        for _page in _page_iterator:
            for _obj in _page['Contents']:
                n_num = n_num + 1
                print("[{}] s3://{}/{}".format(n_num, self._s3_bucket_name, _obj["Key"]))

        print("[Log] s3 total file count : {}".format(n_num))