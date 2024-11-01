import dcql

import json
import os
import logging
import sys

from logger_formatter import CustomFormatter

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)
logger.setLevel(logging.INFO)

def get_test_cases(path):
    return [
        os.path.join(path, f)
        for f in os.listdir(path)
        if os.path.isfile(
            os.path.join(path, f)
        ) and f.startswith("testcase")
    ]


def load_json(path):
    with open(path) as f:
        return json.load(f)


def get_case_num(case):
    filename = os.path.basename(case)
    case_num = int(filename.lstrip("testcase-").rstrip(".json"))
    return case_num


def main():
    test_cases = get_test_cases(os.getcwd())
    test_cases.sort(key=lambda x: get_case_num(x))
    # print('\n'.join(test_cases))
    
    credential_store = load_json("credentials.json")

    for test_path in test_cases:
        test = load_json(test_path)
        logger.info(f"Testing {test_path}: {test['name']}")
        
        matched_credentials = dcql.dcql_query(
            test["dcql_query"],
            credential_store["credentials"]
        )
        logger.info(f"Matched: {json.dumps(matched_credentials, indent=None)}")
        expected_result = test["expected_result"]["matched_credentials"]
        
        if not expected_result == matched_credentials:
            logger.error(f"Expctd: {json.dumps(expected_result)}")
            sys.exit(1)


if __name__ == "__main__":
    main()
