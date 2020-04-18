# -*- coding: utf-8 -*-
import json
from utils import *


class IamHandler():

    def start_main(self):
        _iam_client = Utils.get_client(self, "iam", self._iam_endpoint_url, self._aws_region)

        _exist_result = _iam_client.get_role(
                            RoleName='adminRole'
                        )

        if _exist_result is None:
            _iam_policy = IamHandler.create_iam_policy(self)
            _exist_result = IamHandler.create_iam_role(self, _iam_client, _iam_policy)

        print("[Log-Start] IAM: ", _exist_result.get("Role").get("Arn"))

    def create_iam_role(self, _iam_client, _iam_policy):

        _created_iam_role = _iam_client.create_role(
                                Path='/',
                                RoleName='adminRole',
                                AssumeRolePolicyDocument=_iam_policy,
                                Description='adminRole',
                            )

        return _created_iam_role

    def create_iam_policy(self):

        role_policy_document = json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "Stmt1111111111111",
                    "Action": "*",
                    "Effect": "Allow",
                    "Resource": "*"
                }
            ]
        })

        return role_policy_document