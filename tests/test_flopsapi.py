import mock
import unittest

import inflo


class TestFlopsApi(unittest.TestCase):
    def setUp(self):
        self.api_key = 'test_api_key'
        self.customer_id = 'test_customer_key'
        self.flops = inflo.FlopsApi(self.api_key, self.customer_id)

    @mock.patch('inflo.FlopsApi.send_get_request')
    def test_info(self, get):
        payload_dict = {'status': 'OK'}
        payload_string = '{"status": "OK"}'
        get.return_value = (0, payload_string)
        url = 'test'
        result = self.flops.info(url)
        get.assert_called_with(url, {'clientId': self.customer_id, 'apiKey': self.api_key})
        self.assertEqual(result, payload_dict)

    def test_get_dict_key_correct(self):
        value = self.flops.get_dict_key({'key': 'value'}, 'key')
        self.assertEqual(value, 'value')

    def test_get_dict_key_keyerror(self):
        self.assertRaises(inflo.flops.FlopsJsonNoSuchKeyException, self.flops.get_dict_key, {'key': 'value'}, 'key_1')

    def test_get_dict_key_exception(self):
        self.assertRaises(inflo.flops.FlopsJsonException, self.flops.get_dict_key, 'not_dict', 'key_1')

    def test_deserialize_json_correct(self):
        result = self.flops.deserialize_json('{"status": "OK"}')
        self.assertEqual(result, {'status': 'OK'})

    def test_deserialize_json_exception(self):
        self.assertRaises(inflo.flops.FlopsJsonException, self.flops.deserialize_json, 'not_json')

    @mock.patch('inflo.FlopsApi.info')
    def test_check_inflo_key_false(self, mocked_info):
        vm_id = 1
        mocked_info.return_value = {'status': 'OK', 'result': {'name': 'some_name'}}
        result = self.flops.check_inflo_key(1)
        self.assertFalse(result)

    @mock.patch('inflo.FlopsApi.info')
    def test_check_inflo_key_true(self, mocked_info):
        vm_id = 1
        mocked_info.return_value = {'status': 'OK', 'result': {'name': inflo.FlopsApi.inflo_key+'some_name'}}
        result = self.flops.check_inflo_key(1)
        self.assertTrue(result)

    @mock.patch('inflo.FlopsApi.check_inflo_key')
    @mock.patch('inflo.FlopsApi.send_get_request')
    @mock.patch('inflo.FlopsApi.wait_for_async_answer')
    @mock.patch('inflo.flops.logger')
    def test_shutdown_stopped(self, m_logger, m_wait, m_send_get_request, m_check_inflo_key):
        m_check_inflo_key.return_value = True
        m_send_get_request.return_value = (0, '{"operationId": "3"}')
        m_wait.return_value = (0, 'correct')
        result = self.flops.shutdown(1, 2)
        self.assertEqual(result, 0)
        self.assertTrue(m_logger.info.called)
        m_logger.info.assert_called_with('Operation with ID 3 is finished. Virtual machine with ID 1 is stopped.')

    @mock.patch('inflo.FlopsApi.check_inflo_key')
    @mock.patch('inflo.FlopsApi.send_get_request')
    @mock.patch('inflo.FlopsApi.wait_for_async_answer')
    @mock.patch('inflo.flops.logger')
    def test_shutdown_not_stopped(self, m_logger, m_wait, m_send_get_request, m_check_inflo_key):
        m_check_inflo_key.return_value = False
        m_send_get_request.return_value = (0, '{"operationId": "3"}')
        m_wait.return_value = (0, 'correct')
        result = self.flops.shutdown(1, 2)
        self.assertEqual(result, 1)
        self.assertTrue(m_logger.info.called)
        self.assertTrue(m_logger.debug.called)
        m_logger.info.assert_called_with('No inflo key is in virtual server name, will not stop VM.')
        m_logger.debug.assert_called_with('key_exist value is False, not stopping VM.')

    @mock.patch('inflo.FlopsApi.check_inflo_key')
    @mock.patch('inflo.FlopsApi.send_get_request')
    @mock.patch('inflo.FlopsApi.wait_for_async_answer')
    @mock.patch('inflo.flops.logger')
    def test_shutdown_not_stopped(self, m_logger, m_wait, m_send_get_request, m_check_inflo_key):
        m_check_inflo_key.return_value = True
        m_send_get_request.return_value = (0, '{"operationId": "3"}')
        m_wait.return_value = (1, 'incorrect')
        result = self.flops.shutdown(1, 2)
        self.assertEqual(result, 1)
        self.assertTrue(m_logger.info.called)
        m_logger.info.assert_called_with('Operation with ID 3 is NOT finished. Virtual machine 1 may be NOT stopped. '
                                         'Reason: incorrect')

if __name__ == '__main__':
    unittest.main()
