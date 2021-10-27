provider "aws" {
  region = "eu-west-1"
}

  terraform {
    backend "s3"{
      bucket = "cyber94-gwwirsky-bucket"
      key = "tfstate/calc/terraform.tfstate"
      region = "eu-west-1"
      dynamodb_table = "cyber94_calc_gswirsky_dynamodb_table_lock"
      encrypt = true
    }
  }

# # 1. Create vpc
# @component Dev:PC (#devpc)
# @component CalcApp:VPC (#vpc)

  resource "aws_vpc" "cyber94_calc_gswirsky_vpc_tf" {
    cidr_block = "10.106.0.0/16"
    tags = {
      Name = "cyber94_calc_gswirsky_vpc"
    }
  }

# # 2. Create Internet Gateway
# @component CalcApp:VPC:InternetGateway (#ig)
  resource "aws_internet_gateway" "cyber94_calc_gswirsky_igw_tf" {
    vpc_id = aws_vpc.cyber94_calc_gswirsky_vpc_tf.id


  }
# # 3. Create Custom Route Table
# @component CalcApp:VPC:Route Table (#rt)
# @connects #rt to #ig with Network Traffic
# @connects #ig to #rt with Network Traffic
  resource "aws_route_table" "cyber94_calc_gswirsky_route_table_tf" {
    vpc_id = aws_vpc.cyber94_calc_gswirsky_vpc_tf.id

    route {
      cidr_block = "0.0.0.0/0"
      gateway_id = aws_internet_gateway.cyber94_calc_gswirsky_igw_tf.id
    }

    route {
      ipv6_cidr_block = "::/0"
      gateway_id      = aws_internet_gateway.cyber94_calc_gswirsky_igw_tf.id
    }

    tags = {
      Name = "cyber94_calc_gswirsky_route_table"
    }
  }

# 4. Create a Subnet
# @component CalcApp:VPC:Subnet:App (#subnetapp)
# @connects #rt to #subnetapp with Network Traffic
# @connects #subnetapp to #rt with Network Traffic
  resource "aws_subnet" "cyber94_calc_gswirsky_subnet_app_tf" {
    vpc_id            = aws_vpc.cyber94_calc_gswirsky_vpc_tf.id
    cidr_block        = "10.106.1.0/24"
    availability_zone = "eu-west-1a"

    tags = {
      Name = "cyber94_calc_gswirsky_subnet_app"
    }
  }

# @component CalcApp:VPC:Subnet:Database (#subnetdb)
  resource "aws_subnet" "cyber94_calc_gswirsky_subnet_db_tf" {
    vpc_id            = aws_vpc.cyber94_calc_gswirsky_vpc_tf.id
    cidr_block        = "10.106.2.0/24"
    availability_zone = "eu-west-1a"

    tags = {
      Name = "cyber94_calc_gswirsky_subnet_db"
    }
  }

# @component CalcApp:VPC:Subnet:Bastion (#subnetbs)
# @connects #rt to #subnetbs with Network Traffic
# @connects #subnetbs to #rt with Network Traffic
  resource "aws_subnet" "cyber94_calc_gswirsky_subnet_bastion_tf" {
    vpc_id            = aws_vpc.cyber94_calc_gswirsky_vpc_tf.id
    cidr_block        = "10.106.3.0/24"
    availability_zone = "eu-west-1a"

    tags = {
      Name = "cyber94_calc_gswirsky_subnet_bastion"
    }
  }
 # # 5. Associate subnet with Route Table
  resource "aws_route_table_association" "cyber94_calc_gswirsky_route_table_assoc_app_tf" {
    subnet_id      = aws_subnet.cyber94_calc_gswirsky_subnet_app_tf.id
    route_table_id = aws_route_table.cyber94_calc_gswirsky_route_table_tf.id
  }

  resource "aws_route_table_association" "cyber94_calc_gswirsky_route_table_assoc_bastion_tf" {
    subnet_id      = aws_subnet.cyber94_calc_gswirsky_subnet_bastion_tf.id
    route_table_id = aws_route_table.cyber94_calc_gswirsky_route_table_tf.id
  }

# @component CalcApp:VPC:NACL:App (#naclapp)
# @connects #subnetapp to #naclapp with Are Packets allowed query
# @connects #naclapp to #subnetapp with Are Packets allowed response
  resource "aws_network_acl" "cyber94_calc_gswirsky_nacl_app_tf" {
    vpc_id = aws_vpc.cyber94_calc_gswirsky_vpc_tf.id
    subnet_ids = [aws_subnet.cyber94_calc_gswirsky_subnet_app_tf.id]

    egress {
        protocol   = "tcp"
        rule_no    = 1000
        action     = "allow"
        cidr_block = "0.0.0.0/0"
        from_port  = 3306
        to_port    = 3306
      }
    egress {
        protocol   = "tcp"
        rule_no    = 2000
        action     = "allow"
        cidr_block = "0.0.0.0/0"
        from_port  = 80
        to_port    = 80
      }
    egress {
        protocol   = "tcp"
        rule_no    = 3000
        action     = "allow"
        cidr_block = "0.0.0.0/0"
        from_port  = 443
        to_port    = 443
      }

    egress {
        protocol   = "tcp"
        rule_no    = 4000
        action     = "allow"
        cidr_block = "0.0.0.0/0"
        from_port  = 1024
        to_port    = 65535
      }

    ingress {
        protocol   = "tcp"
        rule_no    = 100
        action     = "allow"
        cidr_block = "0.0.0.0/0"
        from_port  = 443
        to_port    = 443
      }
    ingress {
        protocol   = "tcp"
        rule_no    = 200
        action     = "allow"
        cidr_block = "0.0.0.0/0"
        from_port  = 22
        to_port    = 22
      }
    ingress {
        protocol   = "tcp"
        rule_no    = 300
        action     = "allow"
        cidr_block = "0.0.0.0/0"
        from_port  = 1024
        to_port    = 65535
      }
    tags = {
      Name = "cyber94_calc_gswirsky_nacl_app"
    }
  }

# @component CalcApp:VPC:NACL:Bastion (#naclbs)
# @connects #subnetbs to #naclapp with Are Packets allowed query
# @connects #naclapp to #subnetbs with Are Packets allowed response
  resource "aws_network_acl" "cyber94_calc_gswirsky_nacl_bastion_tf" {
    vpc_id = aws_vpc.cyber94_calc_gswirsky_vpc_tf.id
    subnet_ids      = [aws_subnet.cyber94_calc_gswirsky_subnet_bastion_tf.id]

    egress {
        protocol   = "tcp"
        rule_no    = 1000
        action     = "allow"
        cidr_block = "0.0.0.0/0"
        from_port  = 22
        to_port    = 22
      }

    egress {
        protocol   = "tcp"
        rule_no    = 2000
        action     = "allow"
        cidr_block = "0.0.0.0/0"
        from_port  = 1024
        to_port    = 65535
      }

    ingress {
        protocol   = "tcp"
        rule_no    = 100
        action     = "allow"
        cidr_block = "0.0.0.0/0"
        from_port  = 22
        to_port    = 22
      }
    ingress {
        protocol   = "tcp"
        rule_no    = 200
        action     = "allow"
        cidr_block = "0.0.0.0/0"
        from_port  = 1024
        to_port    = 65535
      }
    tags = {
      Name = "cyber94_calc_gswirsky_nacl_bastion"
    }
  }

# @component CalcApp:VPC:NACL:Database (#nacldb)
# @connects #subnetdb to #nacldb with Are Packets allowed query
# @connects #nacldb to #subnetdb with Are Packets allowed response
  resource "aws_network_acl" "cyber94_calc_gswirsky_nacl_db_tf" {
    vpc_id = aws_vpc.cyber94_calc_gswirsky_vpc_tf.id
    subnet_ids = [aws_subnet.cyber94_calc_gswirsky_subnet_db_tf.id]

    egress {
        protocol   = "tcp"
        rule_no    = 1000
        action     = "allow"
        cidr_block = "0.0.0.0/0"
        from_port  = 1024
        to_port    = 65535
      }

    ingress {
        protocol   = "tcp"
        rule_no    = 100
        action     = "allow"
        cidr_block = "0.0.0.0/0"
        from_port  = 22
        to_port    = 22
      }
    ingress {
        protocol   = "tcp"
        rule_no    = 200
        action     = "allow"
        cidr_block = "0.0.0.0/0"
        from_port  = 3306
        to_port    = 3306
      }
    tags = {
      Name = "cyber94_calc_gswirsky_nacl_db"
    }
  }

 # # 6. Create Security Group to allow port 22,80,443
# @component CalcApp:VPC:SecurityGroup:App (#sgapp)
  resource "aws_security_group" "cyber94_calc_gswirsky_sg_app_tf" {
#    name        = "allow_web_traffic"
#    description = "Allow Web inbound traffic"
    vpc_id      = aws_vpc.cyber94_calc_gswirsky_vpc_tf.id

    ingress {
      description = "SSH"
      from_port   = 22
      to_port     = 22
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
      description = "MySQL"
      from_port   = 3306
      to_port     = 3306
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
      description = "HTTPS"
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
      description = "HTTP"
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
    tags = {
      Name = "cyber94_calc_gswirsky_sg_app"
    }
  }
# @component CalcApp:VPC:SecurityGroup:Bastion (#sgbs)
  resource "aws_security_group" "cyber94_calc_gswirsky_sg_bastion_tf" {
#    name        = "allow_web_traffic"
#    description = "Allow Web inbound traffic"
    vpc_id      = aws_vpc.cyber94_calc_gswirsky_vpc_tf.id

    ingress {
      description = "SSH"
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
      description = "HTTPS"
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
      description = "HTTP"
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
      description = "SSH"
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
      Name = "cyber94_calc_gswirsky_sg_bastion"
    }
  }

# @component CalcApp:VPC:SecurityGroup:Database (#sgdb)
  resource "aws_security_group" "cyber94_calc_gswirsky_sg_db_tf" {
#    name        = "allow_web_traffic"
#    description = "Allow Web inbound traffic"
    vpc_id      = aws_vpc.cyber94_calc_gswirsky_vpc_tf.id

    ingress {
      description = "MySQL"
      from_port   = 3306
      to_port     = 3306
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
      description = "SSH"
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
      from_port   = 0
      to_port     = 0
      protocol    = -1
      cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
      Name = "cyber94_calc_gswirsky_sg_db"
    }
  }

# @component CalcApp:Web:Server (#web_server)
# @connects #web_server to #subnetapp with Network Traffic
# @connects #subnetapp to #web_server with Network Traffic
# @connects #web_server to #sgapp with Is connection allowed query
# @connects #sgapp to #web_server with Is connection allowed response
# @connects #devpc to #web_server with SSH Connection
  resource "aws_instance" "cyber94_calc_gswirsky_server_app_tf" {
    ami = "ami-0943382e114f188e8"
    instance_type = "t2.micro"
    key_name = "cyber94-gwwirsky"
    subnet_id = aws_subnet.cyber94_calc_gswirsky_subnet_app_tf.id
    vpc_security_group_ids = [aws_security_group.cyber94_calc_gswirsky_sg_app_tf.id]
    associate_public_ip_address = true

    tags = {
      Name = "cyber94_calc_gswirsky_server_app"
    }

    lifecycle {
      create_before_destroy = true
    }

    provisioner "remote-exec" {
      inline = [
        "pwd"
      ]
    }

    provisioner "local-exec" {
      working_dir = "../ansible"
      command = "ansible-playbook -i ${self.public_ip}, -u ubuntu playbook0.yml"
    }

  }
# @component CalcApp:Bastion (#bastion)
# @connects #bastion to #subnetbs with Network Traffic
# @connects #subnetbs to #bastion with Network Traffic
# @connects #bastion to #sgbs with Is connection allowed query
# @connects #sgbs to #bastion with Is connection allowed response
# @connects #bastion to #subnetbs with SSH Connection
# @connects #subnetbs to #subnetdb with SSH Connection
# @connects #devpc to #bastion with SSH Connection
  resource "aws_instance" "cyber94_calc_gswirsky_server_bastion_tf" {
    ami = "ami-0943382e114f188e8"
    instance_type = "t2.micro"
    key_name = "cyber94-gwwirsky"
    subnet_id = aws_subnet.cyber94_calc_gswirsky_subnet_bastion_tf.id
    vpc_security_group_ids = [aws_security_group.cyber94_calc_gswirsky_sg_bastion_tf.id]
    associate_public_ip_address = true

    tags = {
      Name = "cyber94_calc_gswirsky_server_bastion"
    }

    lifecycle {
      create_before_destroy = true
    }
  }
# @component CalcApp:Database (#db)
# @connects #subnetdb to #db with SSH Connection
# @connects #db to #sgdb with Is connection allowed query
# @connects #sgdb to #db with Is connection allowed response
  resource "aws_instance" "cyber94_calc_gswirsky_server_db_tf" {
    ami = "ami-0d1c7c4de1f4cdc9a"
    instance_type = "t2.micro"
    key_name = "cyber94-gwwirsky"
    subnet_id = aws_subnet.cyber94_calc_gswirsky_subnet_db_tf.id
    vpc_security_group_ids = [aws_security_group.cyber94_calc_gswirsky_sg_db_tf.id]

    tags = {
      Name = "cyber94_calc_gswirsky_server_db"
    }

    lifecycle {
      create_before_destroy = true
    }
  }









    /*
    connection {
      type = "ssh"
      user = "ubuntu"
      host = self.public_ip
      private_key = file("/home/kali/cyber94-gwwirsky.pem")
    }

    provisioner "file" {
      source = "./docker-install.sh"
      destination = "/home/ubuntu/docker-install.sh"
    }
    provisioner "remote-exec" {
      inline = [
        "chmod 777 /home/ubuntu/docker-install.sh",
        "/home/ubuntu/docker-install.sh"

      ]
    }
    provisioner "remote-exec" {
      inline = [
        "docker run hello-world"
      ]
    }
    */
