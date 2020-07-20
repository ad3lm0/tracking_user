provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

resource "aws_instance" "example" {
  ami           = "ami-2757f631"
  instance_type = "t2.micro"
}

resource "aws_iam_role" "firehose_role_terraform" {
  name = "firehose_test_role"

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

resource "aws_iam_role_policy" "firehose-stream-policy" {
  name = "firehose-stream-policy"
  role = "${aws_iam_role.firehose_role_terraform.id}"

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
              "arn:aws:s3:::event_tracking_user_bucket",
              "arn:aws:s3:::event_tracking_user_bucket/*"
            ]
      }
    ]
}
EOF
}

resource "aws_s3_bucket" "bucket" {
  bucket = "event_tracking_user_bucket"
  acl    = "private"
}

resource "aws_kinesis_firehose_delivery_stream" "alias_stream" {
  name        = "terraform-firehose-alias-stream"
  destination = "s3"

  s3_configuration {
    role_arn   = "${aws_iam_role.firehose_role_terraform.arn}"
    bucket_arn = "${aws_s3_bucket.bucket.arn}"
    prefix = "sucess/alias/batch/"
    buffer_size = "1"
    buffer_interval = "60"
  }
}

resource "aws_kinesis_firehose_delivery_stream" "profile_stream" {
  name        = "terraform-firehose-profile-stream"
  destination = "s3"

  s3_configuration {
    role_arn   = "${aws_iam_role.firehose_role_terraform.arn}"
    bucket_arn = "${aws_s3_bucket.bucket.arn}"
    prefix = "sucess/profile/batch/"
    buffer_size = "1"
    buffer_interval = "60"
  }
}

resource "aws_kinesis_firehose_delivery_stream" "track_stream" {
  name        = "terraform-firehose-track-stream"
  destination = "s3"

  s3_configuration {
    role_arn   = "${aws_iam_role.firehose_role_terraform.arn}"
    bucket_arn = "${aws_s3_bucket.bucket.arn}"
    prefix = "sucess/track/batch/"
    buffer_size = "1"
    buffer_interval = "60"
  }
}