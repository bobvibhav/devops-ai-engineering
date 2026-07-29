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

module "project_a_vpc" {
  source = "./vpc-module"

  vpc_cidr          = "10.0.0.0/16"
  subnet_cidr       = "10.0.1.0/24"
  availability_zone = "ap-south-1a"
  name_prefix       = "project-a"
}

module "project_b_vpc" {
  source = "./vpc-module"

  vpc_cidr          = "10.1.0.0/16"
  subnet_cidr       = "10.1.1.0/24"
  availability_zone = "ap-south-1b"
  name_prefix       = "project-b"
}