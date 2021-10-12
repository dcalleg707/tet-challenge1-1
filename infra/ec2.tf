module "ec2_instance" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 3.0"

  for_each = toset(["100", "101"])

  name = "moises-${each.key}"

  ami                    = "ami-074cce78125f09d61"
  instance_type          = "t2.micro"
  key_name               = var.key_name
  monitoring             = true
  vpc_security_group_ids = [aws_security_group.moises-sg.id]
  subnet_id              = aws_subnet.pub-subnet-1.id
  user_data              = file("files/moises_init.sh")
  private_ip             = "172.16.1.${each.value}"

  tags = {
    Name = "Moises-${each.value}"
  }
}

module "ec2_instance2" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 3.0"

  for_each = toset(["150", "151"])

  name = "hermes-${each.key}"

  ami                    = "ami-074cce78125f09d61"
  instance_type          = "t2.micro"
  key_name               = var.key_name
  monitoring             = true
  vpc_security_group_ids = [aws_security_group.hermes-sg.id]
  subnet_id              = aws_subnet.pub-subnet-1.id
  user_data              = file("files/hermes_init.sh")
  private_ip             = "172.16.1.${each.value}"
  tags = {
    Name = "Hermes-${each.value}"
  }
}

module "ec2_instance3" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 3.0"

  for_each = toset(["200", "201", "202", "203", "204", "205"])

  name = "db-${each.value}"

  ami                    = "ami-074cce78125f09d61"
  instance_type          = "t2.micro"
  key_name               = var.key_name
  monitoring             = true
  vpc_security_group_ids = [aws_security_group.data-server-sg.id]
  subnet_id              = aws_subnet.pub-subnet-1.id
  user_data              = file("files/db_servers_init.sh")
  private_ip             = "172.16.1.${each.value}"
  

  tags = {
    Name = "DB-${each.value}"
  }
}