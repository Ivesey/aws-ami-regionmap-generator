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
    parser.add_argument('images',
                        type=csv,
                        help='comma-separated list of valid AMIs')
    parser.add_argument('-k', '--keys',
                        type=csv,
                        help='comma-separated list of map keys for images (default is AMIx)')
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
    include_exclude_group = parser.add_mutually_exclusive_group()
    include_exclude_group.add_argument('-i', '--include',
                       type=csv,
                       help='comma-separated list of regions to include (default is all)')
    include_exclude_group.add_argument('-e', '--exclude',
                       type=csv,
                       help='comma-separated list of regions to exclude (default is none)')

    args = parser.parse_args()

    map_name = args.name
    images = args.images
    result = {map_name : {}}
    iteration = 0

    for image in images:
        conn = boto.ec2.connect_to_region(args.region)
        current_image = conn.get_image(image)
        name = current_image.name

        try:
            key = args.keys[iteration]
        except (IndexError, TypeError):
            key = 'AMI{}'.format(iteration + 1)

        print_if_verbose('Got: "{}" in "{}"'.format(name, conn.region.name), args.verbose)

        for region in conn.get_all_regions():
            if i_should_query_region(region.name, args.include, args.exclude):
                conn = boto.ec2.connect_to_region(region.name)
                region_images = conn.get_all_images(filters={'name':name})
                for region_image in region_images:
                    if conn.region.name not in result[map_name]:
                        result[map_name][conn.region.name] = {}

                    result[map_name][conn.region.name][key] = region_image.id
                    print_if_verbose(
                        'Got "{}" in "{}"'.format(region_image.id, conn.region.name), args.verbose)
        iteration += 1

    print(json.dumps(result, indent=4))

if __name__ == '__main__':
    main()
