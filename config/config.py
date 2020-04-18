# -*- coding: utf-8 -*-
class Config:
    # Common Config
    _OS_GUBN                  = ["windows","linux"]
    _GUBN                     = "dev"
    _ACCOUNT_NUMBER           = "000000000000"
    _APP_NAME                 = "webLogAnalytics"
    _AWS_REGION               = "us-east-1"
    _LOCALSTACK_IP            = "http://192.168.70.128"

    # AWS S3 Config
    _S3_BUCKET_NAME           = "weblog-output-bucket"
    _S3_PREFIX                = "output"
    _S3_ENDPOINT_URL          = _LOCALSTACK_IP+":"+"4572"

    # AWS Kinesis DataStream Config
    _DATA_STREAM_NAME         = "weblog-kinesis-datastream"
    _DATA_STREAM_ENDPOINT_URL = _LOCALSTACK_IP+":"+"4568"
    _CONSUMER_NAME            = "weblog-consumer-01"

    # AWS Kinesis FireHose Config
    _FIREHOSE_STREAM_NAME     = "weblog-kinesis-firehose-stream"
    _FIREHOST_ENDPOINT_URL    = _LOCALSTACK_IP+":"+"4573"

    # AWS Lambda Config
    _LAMBDA_FUNC_NAME         = "weblog_convert_lambda"
    _LAMBDA_ENDPOINT_URL      = _LOCALSTACK_IP+":"+"4574"
    _LAMBDA_ZIP_PATH          = "C:\\test\\weblog_convert_lambda.zip"
    _LAMBDA_FUNC_PATH         = "C:\\weblog_convert_lambda"

    # File Copy(OS-Windows)
    _COPY_SOURCE_PATH         = r'C:\\Users\\yoo\\PycharmProjects\\WebLogAnalytics\\config\\weblog_convert_lambda.py'
    _COPY_DESTINATION_PATH    = r'C:\\weblog_convert_lambda.py'

    # AWS IAM
    _IAM_NAME                 = "weblog"
    _IAM_ENDPOINT_URL         = _LOCALSTACK_IP+":"+"4593"

    # AWS CloudWatch
    _CW_NAME                  = "cloudwatch"
    _CW_ENDPOINT_URL          = _LOCALSTACK_IP+":"+"4582"

    # AWS CloudWatch Logs
    _CW_LOGS_NAME             = "cloudwatch-logs"
    _CW_LOGS_ENDPOINT_URL     = _LOCALSTACK_IP+":"+"4586"