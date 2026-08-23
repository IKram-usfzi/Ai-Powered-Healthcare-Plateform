# architecture.md §5: single EC2 instance (t2/t3.micro) in the public subnet
# runs the whole app tier via Docker Compose — same infra/docker-compose.yml
# used locally, layered with infra/docker-compose.aws.yml (RDS instead of a
# local postgres container; Prometheus/Grafana trimmed per TRD.md §8).

resource "aws_instance" "app" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.ec2_instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.app.id]
  key_name               = var.ssh_key_name

  root_block_device {
    volume_size = 20
    volume_type = "gp2"
  }

  user_data = templatefile("${path.module}/user_data.sh.tpl", {
    app_repo_url = var.app_repo_url
    db_username  = var.db_username
    db_password  = var.db_password
    db_name      = var.db_name
    rds_endpoint = aws_db_instance.postgres.address
  })

  tags = merge(local.common_tags, { Name = "${var.project_name}-app" })

  depends_on = [aws_db_instance.postgres]
}

# Elastic IP so the public address survives a stop/start (free while
# attached to a running instance — only billed if left unattached).
resource "aws_eip" "app" {
  instance = aws_instance.app.id
  domain   = "vpc"

  tags = merge(local.common_tags, { Name = "${var.project_name}-app-eip" })
}
