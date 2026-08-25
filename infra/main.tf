# Demo-only Terraform-looking configuration.
# Consumed by the local mock Terraform CLI — never sent to AWS or real Terraform.

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type        = string
  description = "AWS region for the customer production database."
  default     = "eu-central-1"
}

variable "aws_account_id" {
  type        = string
  description = "AWS account ID (demo constant)."
  default     = "111122223333"
}

variable "db_identifier" {
  type        = string
  description = "RDS instance identifier."
  default     = "customer-prod"
}

variable "kms_key_id" {
  type        = string
  description = "KMS key ARN used to encrypt the RDS instance."
}

variable "engine" {
  type    = string
  default = "postgres"
}

variable "engine_version" {
  type    = string
  default = "15.4"
}

variable "instance_class" {
  type    = string
  default = "db.r6g.large"
}

resource "aws_db_instance" "customer_prod" {
  identifier     = var.db_identifier
  engine         = var.engine
  engine_version = var.engine_version
  instance_class = var.instance_class

  allocated_storage     = 100
  max_allocated_storage = 500
  storage_encrypted     = true
  kms_key_id            = var.kms_key_id

  db_name  = "customer"
  username = "dbadmin"
  # password omitted — mock only

  multi_az               = true
  publicly_accessible    = false
  deletion_protection    = false
  skip_final_snapshot    = true

  tags = {
    Name        = var.db_identifier
    Environment = "production"
    Owner       = "platform"
    Compliance  = "pci"
  }
}

output "db_instance_arn" {
  value = "arn:aws:rds:${var.aws_region}:${var.aws_account_id}:db:${var.db_identifier}"
}

output "kms_key_id" {
  value = var.kms_key_id
}

# chore: touch for demo trigger
# chore: retrigger after COPILOT_GITHUB_TOKEN update
