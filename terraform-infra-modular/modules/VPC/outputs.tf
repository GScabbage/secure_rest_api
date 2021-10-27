output "output_aws_vpc_id" {
  value = aws_vpc.cyber94_calculator_gswirsky_vpc_tf.id
}

output "output_dns_zone_id" {
  value = aws_route53_zone.cyber94_calculator_gswirsky_vpc_dns_tf.zone_id
}

output "output_internet_route_table" {
  value = aws_route_table.cyber94_calculator_gswirsky_rt_tf.id
}
