output "output_webserver_ip_address" {
  value = aws_instance.cyber94_calculator_gswirsky_webserver_tf.*.public_ip
}
