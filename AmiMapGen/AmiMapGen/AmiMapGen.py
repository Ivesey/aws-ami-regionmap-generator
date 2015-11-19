"""generates a CloudFormation region map for AMIs"""

import boto.ec2
import json
import argparse
import os

def csv(value):
    """split value based on commas. Used in argparser for include / exclude lists"""
    return value.split(',')

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
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--include',
                       type=csv,
                       help='comma-separated list of regions to include (default is all)')
    group.add_argument('-e', '--exclude',
                       type=csv,
                       help='comma-separated list of regions to exclude (default is none)')

    args = parser.parse_args()

    generator = AmiMapGenerator(args.region, args.verbose, args.include, args.exclude)
    result = generator.generate_map(args.name, args.images, args.keys)

    print(json.dumps(result, indent=4))

class AmiMapGenerator:
    """class that does the RegionMap generation"""

    def __init__(self, initial_region, verbose, include, exclude):
        self.verbose = verbose
        self.initial_region = initial_region
        self.include = include
        self.exclude = exclude
        self.check_all = ((include is None) & (exclude is None))
        self.region_cache = {}

    def print_if_verbose(self, message):
        """only print the message if the verbose attribute for this object is True"""
        if self.verbose:
            print(message)

    def i_should_query_region(self, region_to_check):
        """return True if we should be checking this region"""
        if self.check_all:
            return True
        if region_to_check in self.region_cache:
            return True
        if self.include != None:
            if region_to_check in self.include:
                self.region_cache[region_to_check] = True
                return True
        if self.exclude != None:
            if region_to_check not in self.exclude:
                self.region_cache[region_to_check] = True
                return True
        return False

    def generate_map(self, map_name, images, keys):
        """recurse regions and amis to generate the map"""

        result = {map_name : {}}
        iteration = 0
        regions = None

        for image in images:
            conn = boto.ec2.connect_to_region(self.initial_region)
            current_image = conn.get_image(image)
            name = current_image.name

            try:
                key = keys[iteration]
            except (IndexError, TypeError):
                key = 'AMI{}'.format(iteration + 1)

            self.print_if_verbose('Got: "{}" in "{}"'.format(name, conn.region.name))

            if regions is None:
                regions = conn.get_all_regions()

            for region in regions:
                if self.i_should_query_region(region.name):
                    conn = boto.ec2.connect_to_region(region.name)
                    region_images = conn.get_all_images(filters={'name':name})
                    for region_image in region_images:
                        if conn.region.name not in result[map_name]:
                            result[map_name][conn.region.name] = {}

                        result[map_name][conn.region.name][key] = region_image.id
                        self.print_if_verbose(
                            'Got "{}" in "{}"'.format(region_image.id, conn.region.name))
            iteration += 1

        return result

if __name__ == '__main__':
    main()
