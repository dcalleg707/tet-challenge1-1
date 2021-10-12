resource "aws_lb_target_group" "moises-tg" {
  name     = "moises-tg"
  port     = 10000
  protocol = "HTTP"
  target_type = "instance"
  vpc_id   = aws_vpc.main-vpc.id
}

resource "aws_lb_target_group" "hermes-tg" {
  name     = "hermes-tg"
  port     = 11000
  protocol = "HTTP"
  target_type = "instance"
  vpc_id   = aws_vpc.main-vpc.id
}

resource "aws_lb" "db-lb" {
  name               = "db-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb-sg.id]
  subnets            = [aws_subnet.pub-subnet-1.id, aws_subnet.pub-subnet-2.id ]

}

resource "aws_lb_listener" "moises-listener" {
  load_balancer_arn = aws_lb.db-lb.arn
  port              = "10000"
  protocol          = "HTTP"
  

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.moises-tg.arn
  }
}

resource "aws_lb_listener" "hermes-listener" {
  load_balancer_arn = aws_lb.db-lb.arn
  port              = "11000"
  protocol          = "HTTP"
  

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.hermes-tg.arn
  }
}