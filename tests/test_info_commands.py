import json

import mock
import unittest

import inflo

api_key = 'test_api_key'
customer_id = 'test_customer_key'
url = 'http://some.test.url'
operation_id = '1'
raw = True

operation_id_pending_5 = {
    'status': 'OK',
    'result': {
        'id': 1,
        'status': 'PENDING',
        'errorMessage': None,
        'percentage': 5
    }
}

operation_id_pending_50 = {
    'status': 'OK',
    'result': {
        'id': 1,
        'status': 'PENDING',
        'errorMessage': None,
        'percentage': 50
    }
}

operation_id_pending_95 = {
    'status': 'OK',
    'result': {
        'id': 1,
        'status': 'PENDING',
        'errorMessage': None,
        'percentage': 95
    }
}

operation_id_done = {
    'status': 'OK',
    'result': {
        'id': 1,
        'status': 'DONE',
        'errorMessage': None,
        'percentage': 100
    }
}

operation_id_done_result = {
        'id': 1,
        'status': 'DONE',
        'errorMessage': None,
        'percentage': 100
    }

operation_id_error = {
    'status': 'OK',
    'result': {
        'id': 1,
        'status': 'PENDING',
        'errorMessage': 'test_error',
        'percentage': 50
    }
}

operation_id_pending_5_json = json.dumps(operation_id_pending_5)
operation_id_pending_50_json = json.dumps(operation_id_pending_50)
operation_id_pending_95_json = json.dumps(operation_id_pending_95)
operation_id_done_json = json.dumps(operation_id_done)
operation_id_done_result_json = json.dumps(operation_id_done_result)


class TestInfloCommands(unittest.TestCase):
    @mock.patch('inflo.inflo_commands.get_info')
    def test_wait_for_async_answer(self, m_gi):

        m_gi.side_effect = [operation_id_pending_5_json, operation_id_pending_50_json,
                            operation_id_pending_95_json, operation_id_done_json]
        result = inflo.wait_for_async_answer(api_key=api_key, customer_id=customer_id, raw=raw, url=url)
        self.assertEqual(result, (0, operation_id_done_result))


if __name__ == '__main__':
    unittest.main()
