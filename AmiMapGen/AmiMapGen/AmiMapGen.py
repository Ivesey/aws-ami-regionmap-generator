"""generates a CloudFormation region map for AMIs"""

import boto3
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
                        nargs='*',
                        help='(list of) valid AMI image id(s)')
    parser.add_argument('-r', '--region',
                        help='specify the region if "image" is not in your default region',
                        default=os.getenv('AWS_DEFAULT_REGION', DEFAULT_REGION))
    parser.add_argument('-n', '--name',
                        help='specify a name for the region map (default is "RegionMap")',
                        default='RegionMap')
    parser.add_argument('-v', '--verbose',
                        help='verbose mode',
                        action='store_true')
    parser.add_argument('-k', '--keynames',
                        nargs='*',
                        help='(list of) key name(s) (default is "AMIx")')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--include',
                       nargs='*',
                       help='list of regions to include (default is all)')
    group.add_argument('-e', '--exclude',
                       nargs='*',
                       help='list of regions to exclude (default is none)')

    args = parser.parse_args()

    generator = AmiMapGenerator(args.region, args.verbose, args.include, args.exclude)
    result = generator.generate_map(args.name, args.images, args.keynames)

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
        self.ec2 = boto3.resource('ec2', region_name=initial_region)
        self.client = boto3.client('ec2', region_name=initial_region)

    def print_if_verbose(self, message):
        """only print the message if the verbose attribute for this object is True"""
        if self.verbose:
            print(message)

    def query_this_region(self, region_to_check):
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

        key_index = 0

        for image_id in images:
            ami = self.ec2.Image(image_id)
            ami_name = ami.name
            creation_date = ami.creation_date

            self.print_if_verbose('Got: "{}" in "{}"'.format(ami_name, self.initial_region))

            response = self.client.describe_regions()

            try:
                key = keys[key_index]
            except Exception as e:
                key = 'AMI{}'.format(key_index + 1)

            key_index += 1

            for region in response['Regions']:
                region_name = region['RegionName']
                if self.query_this_region(region_name):
                    self.client = boto3.client('ec2', region_name)
                    images = self.client.describe_images(Filters=[{'Name':'name', 'Values':[ami_name]}])
                    try:
                        t = result[map_name][region_name]
                    except KeyError as e:
                        result[map_name][region_name] = {}
                    image = images['Images'][0]['ImageId']
                    result[map_name][region_name][key] = image
                    self.print_if_verbose('Got "{}" in "{}"'.format(image, region_name))

        return result

if __name__ == '__main__':
    main()
