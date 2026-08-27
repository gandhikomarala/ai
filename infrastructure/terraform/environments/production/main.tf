terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.30"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  default = "us-east-1"
}

module "vpc" {
  source = "../../modules/vpc"
  cidr_block = "10.0.0.0/16"
  environment = "production"
}

module "rds_pgvector" {
  source = "../../modules/rds_pgvector"
  vpc_id = module.vpc.vpc_id
  instance_class = "db.r6g.xlarge"
  environment = "production"
}

module "redis" {
  source = "../../modules/redis"
  vpc_id = module.vpc.vpc_id
  node_type = "cache.r6g.large"
  environment = "production"
}
