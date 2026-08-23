terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # No remote backend configured — state stays local (terraform.tfstate,
  # gitignored). Fine for a single-operator capstone stretch deployment;
  # revisit (S3 + DynamoDB lock table) only if multiple people ever apply
  # this concurrently.
}

provider "aws" {
  region = var.aws_region
}
