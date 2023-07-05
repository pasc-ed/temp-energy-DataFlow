# Provider for GCP
provider "google" {
  project = "cr-lab-pedouard-123456789"
  region  = "eu-west1"
  zone    = "eu-west1-b"
}

# Backend using the new gcp bucket
terraform {
  backend "gcs" {
    bucket = "backend-123456789"
    prefix = "terraform/state"
  }
}