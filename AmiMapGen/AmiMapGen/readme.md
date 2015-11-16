#amimapgen
##usage:
`amimapgen.py [-h] [-k KEYS] [-r REGION] [-n NAME] [-v] [-i INCLUDE | -e EXCLUDE] image`

generates a CloudFormation region map for AMIs

##positional arguments:
`images` comma-separated list of valid AMIs

##optional arguments:
`-h, --help` show this help message and exit

`-k KEYS, --keys KEYS` comma-separated list of map keys for images (default is AMIx)

`-r REGION, --region REGION` specify the region if "image(s)" is not in your default region

`-n NAME, --name NAME` specify a name for the region map (default is RegionMap)

`-v, --verbose` verbose mode

`-i INCLUDE, --include INCLUDE` comma-separated list of regions to include (default is all)

`-e EXCLUDE, --exclude EXCLUDE` comma-separated list of regions to exclude (default is none)

##Examples:
###`amimapgen.py ami-69b9941e`
```json
{
    "RegionMap": {
        "ap-northeast-1": {
            "64": "ami-9a2fb89a"
        },
        "ap-southeast-2": {
            "64": "ami-c11856fb"
        },
        "eu-west-1": {
            "64": "ami-69b9941e"
        },
        "ap-southeast-1": {
            "64": "ami-52978200"
        },
        "eu-central-1": {
            "64": "ami-daaeaec7"
        },
        "us-west-1": {
            "64": "ami-cd3aff89"
        },
        "us-west-2": {
            "64": "ami-9ff7e8af"
        },
        "us-east-1": {
            "64": "ami-e3106686"
        },
        "sa-east-1": {
            "64": "ami-3b0c9926"
        }
    }
}
```
###`amimapgen.py ami-69b9941e -v -i eu-west-1,us-east-1,eu-central-1 -n LinuxMap`
```
Got "amzn-ami-hvm-2015.09.0.x86_64-gp2" in "eu-west-1"
Got "ami-69b9941e" in "eu-west-1"
Got "ami-daaeaec7" in "eu-central-1"
Got "ami-e3106686" in "us-east-1"
{
    "LinuxMap": {
        "eu-central-1": {
            "64": "ami-daaeaec7"
        },
        "eu-west-1": {
            "64": "ami-69b9941e"
        },
        "us-east-1": {
            "64": "ami-e3106686"
        }
    }
}
```
###`amimapgen.py ami-69b9941e,ami-2fcbf458 -v -i eu-west-1,eu-central-1 -k Linux`
```
Got: "amzn-ami-hvm-2015.09.0.x86_64-gp2" in "eu-west-1"
Got "ami-69b9941e" in "eu-west-1"
Got "ami-daaeaec7" in "eu-central-1"
Got: "Windows_Server-2012-R2_RTM-English-64Bit-Base-2015.10.26" in "eu-west-1"
Got "ami-2fcbf458" in "eu-west-1"
Got "ami-f2f5f9ef" in "eu-central-1"
{
    "RegionMap": {
        "eu-west-1": {
            "AMI2": "ami-2fcbf458",
            "Linux": "ami-69b9941e"
        },
        "eu-central-1": {
            "AMI2": "ami-f2f5f9ef",
            "Linux": "ami-daaeaec7"
        }
    }
}
```
##NOTES:
1. This is actually my first bit of Pythoning in anger, so apologies if I'm not following certain best practices etc.
1. I haven't bothered with an output file argument. Just pipe the results to a text file if you want to do that.
1. If the script can't find a default region, it defaults to eu-west-1. Feel free to change the variable named DEFAULT_REGION to something more suitable.
