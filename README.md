# User Tracking API

This API receives a json payload with users behavior and stores in AWS S3, the connection between the API and the bucket is done using firehose

## Requirments

Python 3.8

[terraform](https://www.terraform.io/downloads.html)

[pip](https://pip.pypa.io/en/stable/)

[AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) configured


## Installation

On the project folder

terraform:
```bash
terraform init
terraform apply
```
<You'll have to change the bucket name and the bucket arn on the firehose-policy>

Confirm the information when prompted and accept


Python packages:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app\main.py
```

you may change the values at app\cloud_aws\connection_strings.py as needed

the payload and format are described in the swagger file at swagger\swagger.yml

## TODO
- more TESTS!
- Correct behavior on the /profile/ endpoint to merge/update the user attributes as needed
- MORE TESTS!
- Deployable container using Docker
- tests... ?!!


