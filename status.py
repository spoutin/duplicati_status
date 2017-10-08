import argparse
import ipaddress
import json
import sys

import discovery
import models


def parameters(args):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Actions, either discovery or id')
    parser.add_argument('--host', type=ipaddress.ip_address, default='127.0.0.1',
                        help='host ip address of duplicati server')
    parser.set_defaults(discovery=False, id=False)

    a_parser = subparsers.add_parser("discovery")
    a_parser.add_argument("discovery", action='store_true', default=True,
                        help='discovery used to discovery configured backups')

    b_parser = subparsers.add_parser("id")
    b_parser.add_argument("id", type=int,
                        help='backup ID to get details on the selected backup')

    parsed_args = parser.parse_args(args)
    return parsed_args


def determine_options(options):
    if options.discovery:
        result = discovery.discovery(str(options.host))
        list_results = list()
        for r in result:
            list_results.append(r.discovery())
        print(json.dumps(list_results), flush=True)

    elif options.id:
        result = discovery.get_backup_details(options.id, str(options.host))
        print(models.dump_model(result.original_backup_object))


if __name__ == '__main__':
    args = parameters(sys.argv[1:])
    determine_options(args)
