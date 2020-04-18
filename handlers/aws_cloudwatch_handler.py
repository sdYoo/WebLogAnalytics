# -*- coding: utf-8 -*-
from utils import *


class CloudWatchHandler():

    def start_main(self):
        _cw_client = Utils.get_client(self, "logs", self._cw_logs_endpoint_url, self._aws_region)

        _res_logs = CloudWatchHandler.get_logs(self, _cw_client)
        for log_line in _res_logs['events']:
            print("[{}][{}] {}".format(log_line["eventId"], log_line["logStreamName"], log_line["message"]))

        # print("[Log] cloudwatch logs: ", _res_logs)

    def get_logs(self, _cw_client):
        _res_logs = _cw_client.filter_log_events(logGroupName="/aws/lambda/weblog_convert_lambda")
        return _res_logs