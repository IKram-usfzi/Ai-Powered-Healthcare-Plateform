# architecture.md §5: "Security Group: 22 / 80 / 443 only" on the app
# instance; RDS reachable only from that security group, never from the
# internet or a plain CIDR (Security.md §7: "Database not directly
# internet-reachable").

resource "aws_security_group" "app" {
  name        = "${var.project_name}-app-sg"
  description = "GlobalCare app tier (EC2 Docker Compose host) — SSH, HTTP, HTTPS only"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "SSH (restrict to your own IP via ssh_allowed_cidr)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, { Name = "${var.project_name}-app-sg" })
}

resource "aws_security_group" "db" {
  name        = "${var.project_name}-db-sg"
  description = "GlobalCare RDS PostgreSQL — reachable only from the app security group"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "PostgreSQL from the app tier only"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, { Name = "${var.project_name}-db-sg" })
}
