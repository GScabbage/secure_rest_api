resource "aws_subnet" "cyber94_calculator_gswirsky_subnet_web_tf" {
  vpc_id = var.var_aws_vpc_id
  cidr_block = "10.0.133.0/24"

  tags = {
    Name = "cyber94_calculator_gswirsky_subnet_web"
  }
}

resource "aws_route_table_association" "cyber94_calc_gswirsky_route_table_assoc_app_tf" {
  subnet_id      = aws_subnet.cyber94_calculator_gswirsky_subnet_web_tf.id
  route_table_id = var.var_internet_route_table
}
