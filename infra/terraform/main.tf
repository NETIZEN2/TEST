terraform {
  required_version = ">= 1.4.0"
}

provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "backups" {
  bucket = "${var.project}-backups"
  versioning {
    enabled = true
  }
}

variable "aws_region" {
  description = "AWS region"
  default     = "ap-southeast-2"
}

variable "project" {
  description = "Project name"
  default     = "osint-pro"
}
