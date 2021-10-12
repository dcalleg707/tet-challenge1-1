# Create a VPC
resource "aws_vpc" "main-vpc" {
  cidr_block = "172.16.0.0/16"

  tags = {
    "Name" = "main VPC"
  }
}

output "aws_vpc_id" {
  value = "${aws_vpc.main-vpc.id}"
}

# Create the first public subnet
resource "aws_subnet" "pub-subnet-1" {
  vpc_id     = aws_vpc.main-vpc.id
  cidr_block = "172.16.1.0/24"
  availability_zone = "us-east-2a"
  map_public_ip_on_launch = true
  
  tags = {
    Name = "pub-subnet-1"
  }
}

# Create the second public subnet
resource "aws_subnet" "pub-subnet-2" {
  vpc_id     = aws_vpc.main-vpc.id
  cidr_block = "172.16.2.0/24"
  availability_zone = "us-east-2b"
  map_public_ip_on_launch = true

  tags = {
    Name = "pub-subnet-2"
  }
}

# Internet Gateway for main-vpc
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main-vpc.id

  tags = {
    "Name" = "igw"
  }
}

# Create Custom Route Table
resource "aws_route_table" "internet-rtable" {
  vpc_id = aws_vpc.main-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  route {
    ipv6_cidr_block        = "::/0"
    gateway_id             = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "internet-rtable"
  }
}

# Associate public subnets with Route Table
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.pub-subnet-1.id
  route_table_id = aws_route_table.internet-rtable.id
}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.pub-subnet-2.id
  route_table_id = aws_route_table.internet-rtable.id
}

#Route the public subnets traffic through the IGW
resource "aws_route" "internet-access" {
  route_table_id = aws_route_table.internet-rtable.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.igw.id
}