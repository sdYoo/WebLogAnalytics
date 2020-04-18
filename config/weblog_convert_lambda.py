import logging as log
import base64
import datetime

log.basicConfig(filename='./log.txt', level=log.DEBUG)

def get_now_timestamp():
    _dt_timestamp = datetime.datetime.now()
    _dt_timestamp = _dt_timestamp.strftime('%Y/%m/%d %H:%M:%S')
    return _dt_timestamp

def handler(event, context):
    log.info('## ENVIRONMENT VARIABLES')

    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record["kinesis"]["data"])
        print("[kinesis data]", payload)

    print("[Lambda End Time] {} ".format(get_now_timestamp()))

    return {
        "message": "Lambda Process Complete"
    }