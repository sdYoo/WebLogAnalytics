from handlers import *
from utils import *
from threading import Thread
from config import *


class LogPipeline():

    def __init__(self, cls):
        # common
        self._gubn = cls._GUBN
        self._account_number = cls._ACCOUNT_NUMBER
        self._aws_region = cls._AWS_REGION
        self._copy_source_path = cls._COPY_SOURCE_PATH
        self._copy_destination_path = cls._COPY_DESTINATION_PATH
        self._localstack_ip = cls._LOCALSTACK_IP
        # aws s3
        self._s3_bucket_name = cls._S3_BUCKET_NAME
        self._s3_prefix  = cls._S3_PREFIX
        self._s3_endpoint_url = cls._S3_ENDPOINT_URL
        # aws kinesis-datastream
        self._data_stream_name = cls._DATA_STREAM_NAME
        self._data_stream_endpoint_url = cls._DATA_STREAM_ENDPOINT_URL
        self._consumer_name = cls._CONSUMER_NAME
        # aws kinesis-firehose
        self._firehose_stream_name = cls._FIREHOSE_STREAM_NAME
        self._firehose_endpoint_url = cls._FIREHOST_ENDPOINT_URL
        # aws lambda
        self._lambda_func_name = cls._LAMBDA_FUNC_NAME
        self._lambda_endpoint_url = cls._LAMBDA_ENDPOINT_URL
        self._lambda_zip_path = cls._LAMBDA_ZIP_PATH
        self._lambda_func_path = cls._LAMBDA_FUNC_PATH
        # aws iam
        self._iam_name = cls._IAM_NAME
        self._iam_endpoint_url = cls._IAM_ENDPOINT_URL

        # aws cloudwatch & logs
        self._cw_endpoint_url = cls._CW_ENDPOINT_URL
        self._cw_logs_endpoint_url = cls._CW_LOGS_ENDPOINT_URL

    def start_log_pipeline(self):
        # 1. create Utils
        Utils.start_main(self)
        # 2. create IAM
        IamHandler.start_main(self)
        # 3. create S3
        S3Handler.start_main(self)
        # 4. create kinesis datastream
        KinesisDataStreamHandler.start_main(self)
        # 5. create kinesis firehose
        KinesisFirehoseHandler.start_main(self)
        # 6. create Lambda
        LambdaHandler.start_main(self)
        # 7. create cloudwatch logs
        CloudWatchHandler.start_main(self)

    def start_thread(self):
        put_log_thread = Thread(target=KinesisDataStreamHandler.put_log, args=(self,))
        # get_log_thread = Thread(target=KinesisDataStreamHandler.get_log, args=(self,))
        put_log_thread.start()
        # get_log_thread.start()
        put_log_thread.join()
        # get_log_thread.join()

def main():
    log_pipeline = LogPipeline(Config)
    # start to pipeline
    log_pipeline.start_log_pipeline()
    # start to Thread
    log_pipeline.start_thread()

if __name__ == "__main__":
    main()