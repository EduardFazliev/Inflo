import json

import mock
import unittest

import inflo
from inflo.inflo_commands import inflo_delete_key

api_key = 'test_api_key'
customer_id = 'test_customer_key'
url = 'http://some.test.url'
operation_id = '1'
raw = True
tenant_id = 1
vm_id = 1

# GET Request responses
success_response = (200, '{"status" : "OK", "operationID" : 1}')

operation_id_pending_5 = (
    '{"status" : "OK", "result" : {"id" : 1, "status" : "PENDING", "errorMessage" :  null, "percentage" : 5}}'
)
operation_id_pending_50 = (
    '{"status" : "OK", "result" : {"id" : 1, "status" : "PENDING", "errorMessage" : null, "percentage" : 50}}'
)
operation_id_pending_95 = (
    '{"status" : "OK", "result" : {"id" : 1, "status" : "PENDING", "errorMessage" : null, "percentage" : 95}}'
)
operation_id_done = (
    '{"status" : "OK", "result" : {"id" : 1, "status" : "DONE", "errorMessage" : null, "percentage" : 100}}'
)
operation_id_done_result = {u'status': u'DONE', u'percentage': 100, u'errorMessage': None, u'id': 1}
operation_id_error = (
    '{"status" : "OK", "result" : {"id" : 1, "status" : "PENDING", "errorMessage" : "test_error", "percentage" : 50}}'
)

deleted_vm_info_no_delete_key = '{"status" : "OK", "result" : {"name" : "test_name" }}'

deleted_vm_info_with_delete_key = '{"status" : "OK", "result" : { "name" : "'+inflo_delete_key+'test_name" }}'


class TestInfloCommands(unittest.TestCase):
    @mock.patch('inflo.requests_lib.send_get_request')
    @mock.patch('inflo.inflo_commands.get_info')
    def test_wait_for_async_answer_correct(self, m_gi, m_sgr):
        m_gi.side_effect = [operation_id_pending_5, operation_id_pending_50, operation_id_pending_95, operation_id_done]
        m_sgr.return_value = success_response

        result = inflo.wait_for_async_answer(api_key=api_key, customer_id=customer_id, raw=raw, url=url)
        self.assertEqual(result, (0, operation_id_done_result))

    @mock.patch('inflo.requests_lib.send_get_request')
    @mock.patch('inflo.inflo_commands.get_info')
    def test_delete_vm_no_delete_key(self, m_gi, m_sgr):
        # We expect this result.
        expected_result = (0, 'No delete key in VM name. VM is NOT deleted.')

        m_gi.return_value = deleted_vm_info_no_delete_key
        m_sgr.return_value = success_response

        result = inflo.delete_vm(vm_id=vm_id, api_key=api_key, customer_id=customer_id, raw=raw, tenant_id=tenant_id)

        self.assertEqual(result, expected_result)

    @mock.patch('inflo.requests_lib.send_get_request')
    @mock.patch('inflo.inflo_commands.get_info')
    def test_delete_vm_with_delete_key(self, m_gi, m_sgr):
        expected_result = (0, 'VM is successfully deleted.')

        m_gi.return_value = deleted_vm_info_with_delete_key
        m_sgr.return_value = success_response

        result = inflo.delete_vm(vm_id=vm_id, api_key=api_key, customer_id=customer_id, raw=raw, tenant_id=tenant_id)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
