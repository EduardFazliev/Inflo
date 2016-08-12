import inflo
import unittest
import mock
import inflo.parser
api_key = 'test_key'
customer_id = 'test_id'
vm_id = 'test_vm_id'
table_format = ['header1', 'header2']
# args =

class TestInflo(unittest.TestCase):
    def setUp(self):
        pass

    def test_inflo_invoke_get_tenant(self):
        inflo.get_tenant_info = mock.MagicMock(return_value=0)
#        inflo.parser.invoke_get_tenant_info()