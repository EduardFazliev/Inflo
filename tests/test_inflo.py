import argparse
import inflo
import unittest
import mock
import inflo.parser


api_key = 'test_key'
customer_id = 'test_id'
vm_id = 'test_vm_id'
table_format = ['header1', 'header2']

script_args = ['-a', api_key, '-i', customer_id, 'tenant-info']
args = argparse.Namespace(api_key=api_key, customer_id=customer_id, raw=False,
                          url='https://api.flops.ru/api/v1/tenant/', table_format=['id', 'description'])
# args =


class TestInflo(unittest.TestCase):
    def setUp(self):
        pass

    def test_inflo_invoke_get_tenant(self):
        inflo.get_info = mock.MagicMock(return_value=0)
        inflo.parser.invoke_get_tenant_info(args)
        inflo.get_info.assert_called_with(api_key=api_key, customer_id=customer_id, raw=False,
                                          url='https://api.flops.ru/api/v1/tenant/', table_format=['id', 'description'])
