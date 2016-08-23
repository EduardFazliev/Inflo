import argparse
import logging
import sys

import inflo
from flops import FlopsApi


logger = logging.getLogger(__name__)
api_link = FlopsApi.api_link


def invoke_get_tenant_info(args):
    """
    This function prints info about available tenants.

    Args:
        args: Arguments, received from arpgparse object.
    """
    url = '{0}tenant/'.format(api_link)
    flops = FlopsApi(args.api_key, args.customer_id)
    flops.info(url)


def invoke_server_list(args):
    """
    This function prints list of available servers.

    Args:
        args: Arguments, received from arpgparse object.
    """
    url = '{0}vm/'.format(api_link)
    flops = FlopsApi(args.api_key, args.customer_id)
    flops.info(url)


def invoke_get_vm_info(args):
    """
    This function prints info about virtual server.

    Args:
        args: Arguments, received from arpgparse object.
    """
    url = '{0}vm/{1}/'.format(api_link, args.vm_id)
    flops = FlopsApi(args.api_key, args.customer_id)
    flops.info(url)


def invoke_os_list(args):
    """
    This function prints list of distributions, available to install.

    Args:
        args: Arguments, received from arpgparse object.
    """
    url = '{0}distribution/'.format(api_link)
    flops = FlopsApi(args.api_key, args.customer_id)
    flops.info(url)


def invoke_get_vm_snapshots(args):
    url = '{0}vm/{1}/snapshots/'.format(api_link, args.vm_id)
    flops = FlopsApi(args.api_key, args.customer_id)
    flops.info(url)


def invoke_get_vm_backups(args):
    url = '{0}vm/{1}/backups/'.format(api_link, args.vm_id)
    flops = FlopsApi(args.api_key, args.customer_id)
    flops.info(url)


def invoke_get_pubkeys(args):
    url = '{0}pubkeys/'.format(api_link)
    flops = FlopsApi(args.api_key, args.customer_id)
    flops.info(url)


def invoke_get_software(args):
    url = '{0}software/'.format(api_link)
    flops = FlopsApi(args.api_key, args.customer_id)
    flops.info(url)


def invoke_get_tariffs(args):
    url = '{0}tariffs/'.format(api_link)
    flops = FlopsApi(args.api_key, args.customer_id)
    flops.info(url)


def invoke_create_vm(args):
    logger.debug('Args list for create virtual server:\n{0}'.format(args))
    flops = FlopsApi(args.api_key, args.customer_id)
    flops.create_vm(args.name, args.tenant_id, args.distr_id, args.tariff_id, args.memory, args.disk, args.cpu,
                    args.ip_count, args.password, args.send_password, args.open_support_access, args.public_key_id,
                    args.software_id)


def invoke_delete_vm(args):
    flops = FlopsApi(args.api_key, args.customer_id)
    flops.delete_vm(args.vm_id, args.tenant_id)


#def invoke_start_vm(args):
#    inflo.start_server(args.vm_id, args.tenant_id, api_key=args.api_key, customer_id=args.customer_id, raw=args.raw)
def set_logger(verbosity):
    if verbosity:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def invoke_parser(script_args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase verbosity.')
    parser.add_argument('-r', '--raw', action='store_true', help='Perform raw json output')
    parser.add_argument('-a', '--api-key', type=str, help='API key.')
    parser.add_argument('-i', '--customer-id', type=str, help='Client ID.')

    subparsers = parser.add_subparsers()

    tenant_info = subparsers.add_parser('tenant-info', help='Get tenant info.')
    tenant_info.set_defaults(func=invoke_get_tenant_info)

    os_list = subparsers.add_parser('os-list', help='Get tenant info.')
    os_list.set_defaults(func=invoke_os_list)

    pubkey_list = subparsers.add_parser('pubkeys', help='Get list of avaliable pubkeys.')
    pubkey_list.set_defaults(func=invoke_get_pubkeys)

    server_list = subparsers.add_parser('server-list', help='Get list of existing servers.')
    server_list.set_defaults(func=invoke_server_list)

    vm_info = subparsers.add_parser('vm-info', help='Get virtual machine info from given vm-id.')
    vm_info.add_argument('--vm-id', type=str, help='Virtual machine ID.', default=None)
    vm_info.set_defaults(func=invoke_get_vm_info)

    vm_snapshots = subparsers.add_parser('vmsnapshot-list', help='Get virtual machine snapshot list.')
    vm_snapshots.add_argument('--vm-id', type=str, help='Virtual machine ID.', default=None)
    vm_snapshots.set_defaults(func=invoke_get_vm_snapshots)

    vm_backup = subparsers.add_parser('vmbackup-list', help='Get virtual machine backup list.')
    vm_backup.add_argument('--vm-id', type=str, help='Virtual machine ID.', default=None)
    vm_backup.set_defaults(func=invoke_get_vm_backups)

    software_list = subparsers.add_parser('software-list', help='Get available software list.')
    software_list.set_defaults(func=invoke_get_software)

    tariff_list = subparsers.add_parser('tariff-list', help='Get available tariff list.')
    tariff_list.set_defaults(func=invoke_get_tariffs)

    create_vm = subparsers.add_parser('create-vm', help='Create virtual server.')
    create_vm.add_argument('--name', type=str, help='Name of virtual server.', default='inflo_created_test_vm')
    create_vm.add_argument('--tenant-id', type=int, help='Tenant(project) ID.', default=28194)
    create_vm.add_argument('--distr-id', type=int, help='Number of distribution ID. List of distributions can be'
                                                        'obtained with "os-list" command', default=311)
    create_vm.add_argument('--tariff-id', type=str, help='Number of tariff ID. List of tariffs can be obtained with'
                                                         '"tariff-list" command.', default=1)
    create_vm.add_argument('--memory', type=int, help='Memory size in MB from 512 to 16384', default=512)
    create_vm.add_argument('--disk', type=int, help='Disk size in MB, from 8192 to 524288.', default=8192)
    create_vm.add_argument('--cpu', type=int, help='Count of CPU cores, from 1 to 12.', default=1)
    create_vm.add_argument('--ip-count', type=int, help='Number of IP addresses, from 0 to 2.', default=1)
    create_vm.add_argument('--password', type=str, help='Password to server, must contain capital and small latin'
                                                        'letters and at least one of symbols ("!","(",")","[","]","-",'
                                                        '".","?","~","`")', default='Hurma228!')
    create_vm.add_argument('--send-password', action='store_true', help='Send password on email.')
    create_vm.add_argument('--open-support-access', action='store_true', help='Open access to virtual'
                                                                              'server to support.')
    create_vm.add_argument('--public-key-id', type=str, help='Public key to add ID. You can obtain list of available'
                                                             'public keys via command "pk-list".', default=None)
    create_vm.add_argument('--software-id', type=str, help='List of available software.', default=None)
    create_vm.set_defaults(func=invoke_create_vm)

    delete_vm = subparsers.add_parser('delete-vm', help='Delete server.')
    delete_vm.add_argument('--vm-id', type=int, help='Virtual server ID to delete.')
    delete_vm.add_argument('--tenant-id', type=int, help='Tenant ID.')
    delete_vm.set_defaults(func=invoke_delete_vm)

#    start_vm = subparsers.add_parser('start-vm', help='Delete server.')
#    start_vm.add_argument('--vm-id', type=int, help='Virtual server ID to delete.')
#    start_vm.add_argument('--tenant-id', type=int, help='Tenant ID.')
#    start_vm.set_defaults(func=invoke_start_vm)

    args = parser.parse_args(script_args)
    set_logger(args.verbose)
    args.func(args)


if __name__ == '__main__':
    pass
