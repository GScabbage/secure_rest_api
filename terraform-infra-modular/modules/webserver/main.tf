resource "aws_security_group" "cyber94_calculator_gswirsky_webserver_sg_tf" {
  name = "cyber94_calculator_gswirsky_webserver_sg"

  vpc_id=var.var_aws_vpc_id

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "cyber94_calculator_gswirsky_webserver_sg"
  }
}

resource "aws_instance" "cyber94_calculator_gswirsky_webserver_tf" {
  ami = var.var_aws_ami_ubuntu_1804
  instance_type = "t2.micro"
  subnet_id = var.var_web_subnet_id
  count = 2
  associate_public_ip_address = true

  key_name = var.var_ssh_key_name

  vpc_security_group_ids = [aws_security_group.cyber94_calculator_gswirsky_webserver_sg_tf.id]

  user_data = templatefile("../init-scripts/dockerinstall.sh", {SPECIAL_ARG="This is an argument from terraform"})
  tags = {
    Name = "cyber94_calculator_gswirsky_webserver_${count.index}"
  }
}

resource "aws_route53_record" "cyber94_calculator_gswirsky_webserver_dns_tf" {
  zone_id = var.var_dns_zone_id
  name = "www"
  type = "A"
  ttl = "30"
  records = aws_instance.cyber94_calculator_gswirsky_webserver_tf.*.public_ip
}
