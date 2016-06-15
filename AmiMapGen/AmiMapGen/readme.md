#amimapgen
##usage:
`amimapgen.py [-h] [-k KEYS] [-r REGION] [-n NAME] [-v] [-i INCLUDE | -e EXCLUDE] images`

generates a CloudFormation region map for AMIs

##positional arguments:
`images` comma-separated list of valid AMIs

##optional arguments:
`-h, --help` show this help message and exit

`-k KEYS, --keys KEYS` list of map keys for images (default is AMIx)

`-r REGION, --region REGION` specify the region if "image(s)" is not in your default region

`-n NAME, --name NAME` specify a name for the region map (default is RegionMap)

`-v, --verbose` verbose mode

`-i INCLUDE, --include INCLUDE` list of regions to include (default is all)

`-e EXCLUDE, --exclude EXCLUDE` list of regions to exclude (default is none)

##Examples:
###`amimapgen.py ami-69b9941e`
```json
{
    "RegionMap": {
        "sa-east-1": {
            "AMI1": "ami-3b0c9926"
        },
        "us-west-2": {
            "AMI1": "ami-9ff7e8af"
        },
        "eu-west-1": {
            "AMI1": "ami-69b9941e"
        },
        "us-east-1": {
            "AMI1": "ami-e3106686"
        },
        "ap-northeast-1": {
            "AMI1": "ami-9a2fb89a"
        },
        "us-west-1": {
            "AMI1": "ami-cd3aff89"
        },
        "ap-southeast-2": {
            "AMI1": "ami-c11856fb"
        },
        "ap-southeast-1": {
            "AMI1": "ami-52978200"
        },
        "eu-central-1": {
            "AMI1": "ami-daaeaec7"
        },
        "ap-northeast-2": {
            "AMI1": "ami-83d419ed"
        }
    }
}
```
###`amimapgen.py ami-69b9941e -v -i eu-west-1 us-east-1 eu-central-1 -n LinuxMap`
```
Got: "amzn-ami-hvm-2015.09.0.x86_64-gp2" in "eu-west-1"
Got "ami-69b9941e" in "eu-west-1"
Got "ami-daaeaec7" in "eu-central-1"
Got "ami-e3106686" in "us-east-1"
{
    "LinuxMap": {
        "eu-central-1": {
            "AMI1": "ami-daaeaec7"
        },
        "us-east-1": {
            "AMI1": "ami-e3106686"
        },
        "eu-west-1": {
            "AMI1": "ami-69b9941e"
        }
    }
}
```
###`amimapgen.py ami-69b9941e ami-29eb7e5a -v -i eu-west-1 eu-central-1 -k Linux`
```
Got: "amzn-ami-hvm-2015.09.0.x86_64-gp2" in "eu-west-1"
Got "ami-69b9941e" in "eu-west-1"
Got "ami-daaeaec7" in "eu-central-1"
Got: "Windows_Server-2012-R2_RTM-English-64Bit-Base-2016.05.11" in "eu-west-1"
Got "ami-29eb7e5a" in "eu-west-1"
Got "ami-827d90ed" in "eu-central-1"
{
    "RegionMap": {
        "eu-west-1": {
            "AMI2": "ami-29eb7e5a",
            "Linux": "ami-69b9941e"
        },
        "eu-central-1": {
            "AMI2": "ami-827d90ed",
            "Linux": "ami-daaeaec7"
        }
    }
}
```
##NOTES:
1. This is actually my first bit of Pythoning in anger, so apologies if I'm not following certain best practices etc.
1. I haven't bothered with an output file argument. Just pipe the results to a text file if you want to do that.
1. If the script can't find a default region, it defaults to eu-west-1. Feel free to change the variable named DEFAULT_REGION to something more suitable.
