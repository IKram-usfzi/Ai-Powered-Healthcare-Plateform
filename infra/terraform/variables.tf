variable "aws_region" {
  description = "AWS region to deploy into. us-east-1 has the broadest Free Tier service availability."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Prefix applied to every resource name/tag, so this stack is identifiable and easy to tear down."
  type        = string
  default     = "globalcare"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.20.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet (EC2 app tier)."
  type        = string
  default     = "10.20.1.0/24"
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for the private subnets (RDS). RDS requires a DB subnet group spanning at least 2 AZs even for a single-AZ instance."
  type        = list(string)
  default     = ["10.20.11.0/24", "10.20.12.0/24"]
}

variable "ec2_instance_type" {
  description = "EC2 instance type for the app tier. t3.micro / t2.micro are Free Tier eligible."
  type        = string
  default     = "t3.micro"
}

variable "db_instance_class" {
  description = "RDS instance class. db.t3.micro / db.t4g.micro are Free Tier eligible."
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "PostgreSQL database name — must match POSTGRES_DB used by the backend."
  type        = string
  default     = "globalcare"
}

variable "db_username" {
  description = "PostgreSQL master username."
  type        = string
  default     = "globalcare"
}

variable "db_password" {
  description = "PostgreSQL master password. No default on purpose — set via terraform.tfvars (gitignored) or TF_VAR_db_password, never committed."
  type        = string
  sensitive   = true
}

variable "ssh_key_name" {
  description = "Name of an existing EC2 key pair (create it in the AWS console/CLI first: `aws ec2 create-key-pair ...`) used for SSH access to the app instance."
  type        = string
}

variable "ssh_allowed_cidr" {
  description = "CIDR allowed to SSH into the app instance (port 22). Restrict to your own IP (e.g. \"203.0.113.4/32\") — never leave this at 0.0.0.0/0 for anything beyond a short-lived demo."
  type        = string
}

variable "app_repo_url" {
  description = "Git URL the EC2 instance clones on boot to get infra/docker-compose.yml and the app source."
  type        = string
  default     = "https://github.com/IKram-usfzi/Ai-Powered-Healthcare-Plateform.git"
}

variable "budget_limit_usd" {
  description = "Monthly budget cap in USD that triggers the AWS Budgets alarm (Security.md §7 / TRD.md §8: 'AWS Budgets billing alarm configured before any deployment activity')."
  type        = string
  default     = "10"
}

variable "budget_alert_email" {
  description = "Email address that receives the budget threshold alert. No default on purpose — must be set explicitly."
  type        = string
}
