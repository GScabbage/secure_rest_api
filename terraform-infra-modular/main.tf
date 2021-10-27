provider "aws" {
  region=var.var_region
}

terraform {
  backend "s3"{
    bucket = "cyber94-gwwirsky-bucket"
    key = "tfstate/calc/terraform.tfstate"
    region = "eu-west-1"
    dynamodb_table = "cyber94_calculator_gswirsky_dynamodb_table_lock"
    encrypt = true
  }
}

module "VPC" {
  source = "./modules/VPC"
}

module "web_subnet" {
  source = "./modules/web_subnet"

  var_aws_vpc_id = module.VPC.output_aws_vpc_id
  var_internet_route_table = module.VPC.output_internet_route_table
}

module "webserver" {
  source = "./modules/webserver"

  var_web_subnet_id = module.web_subnet.output_web_subnet_id
  var_ssh_key_name = var.var_ssh_key_name
  var_dns_zone_id = module.VPC.output_dns_zone_id

  var_aws_vpc_id = module.VPC.output_aws_vpc_id
}
