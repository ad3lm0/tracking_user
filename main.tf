provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_instance" "example" {
  ami           = "ami-2757f631"
  instance_type = "t2.micro"
}

resource "aws_iam_role" "firehose_role_userbehavior" {
  name = "firehose_userbehavior_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "firehose.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "firehose-userbheavior-stream-policy" {
  name = "firehose-userbheavior-stream-policy"
  role = "${aws_iam_role.firehose_role_userbehavior.id}"

 policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
       {
            "Effect": "Allow",
            "Action": "kinesis:*",
            "Resource": "*"
        },
	    {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
              "arn:aws:s3:::behavior-tracking-user-bucket",
              "arn:aws:s3:::behavior-tracking-user-bucket/*"
            ]
      }
    ]
}
EOF
}

resource "aws_s3_bucket" "bucket" {
  bucket = "behavior-tracking-user-bucket"
  acl    = "private"
}

resource "aws_kinesis_firehose_delivery_stream" "alias_stream" {
  name        = "firehose-alias-stream"
  destination = "s3"

  s3_configuration {
    role_arn   = "${aws_iam_role.firehose_role_userbehavior.arn}"
    bucket_arn = "${aws_s3_bucket.bucket.arn}"
    prefix = "success/alias/batch/"
    buffer_size = "1"
    buffer_interval = "60"
  }
}

resource "aws_kinesis_firehose_delivery_stream" "profile_stream" {
  name        = "firehose-profile-stream"
  destination = "s3"

  s3_configuration {
    role_arn   = "${aws_iam_role.firehose_role_userbehavior.arn}"
    bucket_arn = "${aws_s3_bucket.bucket.arn}"
    prefix = "success/profile/batch/"
    buffer_size = "1"
    buffer_interval = "60"
  }
}

resource "aws_kinesis_firehose_delivery_stream" "track_stream" {
  name        = "firehose-track-stream"
  destination = "s3"

  s3_configuration {
    role_arn   = "${aws_iam_role.firehose_role_userbehavior.arn}"
    bucket_arn = "${aws_s3_bucket.bucket.arn}"
    prefix = "success/track/batch/"
    buffer_size = "1"
    buffer_interval = "60"
  }
}