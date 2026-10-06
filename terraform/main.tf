terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "neurolake_bucket" {
  name          = "${var.project_id}-neurolake-storage"
  location      = var.region
  force_destroy = true
  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "raw_dataset" {
  dataset_id = "neurolake_raw"
  location   = var.region
}

resource "google_bigquery_dataset" "analytics_dataset" {
  dataset_id = "neurolake_analytics"
  location   = var.region
}
