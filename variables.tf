# Variable for generic bucket
variable "files_bucket_name" {
  type    = string
  default = "generic-files-123456798"
}

variable "project_id" {
  type    = string
  default = "cr-lab-pedouard-123456798"
}

variable "region" {
  type    = string
  default = "europe-west1"
}

variable "template_file_name" {
  type    = string
  default = "temperature-preprocessing"
}

variable "dataset_id" {
  type    = string
  default = "temperature"
}

variable "table_id" {
  type    = string
  default = "temperature"
}