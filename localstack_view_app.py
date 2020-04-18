from handlers import *
from config import *
from flask import Flask, render_template

app = Flask(__name__)


def get_logs(_cw_client):
    _res_logs = _cw_client.filter_log_events(logGroupName="/aws/lambda/weblog_convert_lambda")
    return _res_logs


def get_client(_aws_service, _endpoint_url, _region_name):
    _aws_service_client = boto3.client(_aws_service,
                                       endpoint_url=_endpoint_url,
                                       use_ssl=False,
                                       region_name=_region_name)
    return _aws_service_client


@app.route('/list')
def describe_detail_data():
    _cw_client = get_client("logs", Config._CW_LOGS_ENDPOINT_URL, Config._AWS_REGION)
    _res_logs = get_logs(_cw_client)

    _cw_list = []
    _row_num = 1

    for log_line in _res_logs['events']:
        # print("[{}][{}] {}".format(log_line["eventId"], log_line["logStreamName"], log_line["message"]))
        _cw_list.append(
            {
                "rowNumber":_row_num,
                "eventId":log_line["eventId"],
                "logStreamName":log_line["logStreamName"],
                "message":log_line["message"]
            }
        )
        _row_num = _row_num+1

    # _cw_list.sort(reverse=True)

    return render_template('localstack_viewer.html', cw_list=_cw_list)


if __name__ == '__main__':
    app.run('0.0.0.0',7001)
