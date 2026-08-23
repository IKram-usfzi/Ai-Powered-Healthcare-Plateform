# architecture.md §5 / TRD.md §8: single-AZ RDS PostgreSQL in the private
# subnet. Free Tier eligible sizing (db.t3.micro/db.t4g.micro, 20GB gp2,
# single-AZ — Multi-AZ is NOT Free Tier eligible and is intentionally not
# used here).

resource "aws_db_instance" "postgres" {
  identifier     = "${var.project_name}-db"
  engine         = "postgres"
  engine_version = "16"

  instance_class    = var.db_instance_class
  allocated_storage = 20
  storage_type      = "gp2"

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]

  multi_az            = false
  publicly_accessible = false
  storage_encrypted   = true

  backup_retention_period = 1
  skip_final_snapshot     = true
  deletion_protection     = false

  tags = merge(local.common_tags, { Name = "${var.project_name}-db" })
}
