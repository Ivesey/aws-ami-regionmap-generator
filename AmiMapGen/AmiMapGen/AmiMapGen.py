"""generates a CloudFormation region map for AMIs"""

import boto.ec2
import json
import argparse
import os

def print_if_verbose(message, verbose):
    """only print the message if the verbose arg is True"""
    if verbose:
        print(message)

def csv(value):
    """split value based on commas. Used in argparser for include / exclude lists"""
    return value.split(',')

def i_should_query_region(region_to_check, include, exclude):
    """return True if we should be checking this region"""
    if (include is None) & (exclude is None):
        return True
    if include != None:
        return region_to_check in include
    if exclude != None:
        return region_to_check not in exclude

DEFAULT_REGION = 'eu-west-1'
"""I'd call this the default default region"""

def main():
    """generates the region map and dumps it as JSON"""
    parser = argparse.ArgumentParser(description='generates a CloudFormation region map for AMIs')
    parser.add_argument('image',
                        help='a valid AMI image id')
    parser.add_argument('-r', '--region',
                        help='specify the region if "image" is not in your default region',
                        default=os.getenv('AWS_DEFAULT_REGION',
                                          boto.config.get('Boto', 'ec2_region_name',
                                                          DEFAULT_REGION)))
    parser.add_argument('-n', '--name',
                        help='specify a name for the region map (default is "RegionMap")',
                        default='RegionMap')
    parser.add_argument('-v', '--verbose',
                        help='verbose mode',
                        action='store_true')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--include',
                       type=csv,
                       help='comma-separated list of regions to include (default is all)')
    group.add_argument('-e', '--exclude',
                       type=csv,
                       help='comma-separated list of regions to exclude (default is none)')

    args = parser.parse_args()

    map_name = args.name
    conn = boto.ec2.connect_to_region(args.region)
    image = conn.get_image(args.image)
    name = image.name
    result = {map_name : {}}

    print_if_verbose('Got: "{}" in "{}"'.format(name, conn.region.name), args.verbose)

    for region in conn.get_all_regions():
        if i_should_query_region(region.name, args.include, args.exclude):
            conn = boto.ec2.connect_to_region(region.name)
            images = conn.get_all_images(filters={'name':name})
            for image in images:
                if conn.region.name not in result[map_name]:
                    result[map_name][conn.region.name] = {}
                arch = '64'
                if image.architecture != 'x86_64':
                    arch = '32'
                result[map_name][conn.region.name][arch] = image.id
                print_if_verbose(
                    'Got "{}" in "{}"'.format(image.id, conn.region.name), args.verbose)

    print(json.dumps(result, indent=4))

if __name__ == '__main__':
    main()
