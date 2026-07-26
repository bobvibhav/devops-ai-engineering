terraform {

    required_providers {
        aws = {

            source  = "hashicorp/aws"
            version = "~> 5.0"
        }
    }

}

provider "aws"{
    region = "ap-south-1"
    }

resource "aws_s3_bucket" "my_first_bucket" {
  bucket = "vibhav-terraform-demo-bucket-2026"
}