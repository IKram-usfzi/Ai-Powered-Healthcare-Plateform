data "aws_availability_zones" "available" {
  state = "available"
}

# Latest Ubuntu 22.04 LTS AMI (Canonical's official account) — kept unpinned
# to a specific AMI ID so a fresh `terraform apply` always boots current
# security patches, consistent with this project's "pin dependencies, not
# base images that need patching" balance (see deccission.md ADR-026's
# Trivy-scan note on periodic base-image rescans).
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

locals {
  common_tags = {
    Project     = var.project_name
    ManagedBy   = "terraform"
    Environment = "aws-stretch"
  }
}
