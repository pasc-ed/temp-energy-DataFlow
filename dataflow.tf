# Setup Dataflow pipeline
resource "google_dataflow_job" "dataflow" {
  name                    = "tf-infra-job"
  template_gcs_path       = "gs://${var.files_bucket_name}/template-file/${var.template_file_name}.json"
  temp_gcs_location       = "gs://${var.files_bucket_name}/temp-location"
  region                  = var.region
  enable_streaming_engine = false
  zone                    = "europe-west1-a"
  parameters = {
    dataset_id      = google_bigquery_dataset.dataset.dataset_id
    table_id        = google_bigquery_table.table.table_id
    raw_data_bucket = google_storage_bucket.raw_data_bucket.name
  }
}

resource "google_project_iam_member" "compute_engine_service_account" {
  project = var.project_id
  role    = "roles/dataflow.worker"
  member  = "serviceAccount:${data.google_project.current.number}-compute@developer.gserviceaccount.com"
}

resource "google_project_iam_member" "dataflow_admin" {
  project = var.project_id
  role    = "roles/dataflow.admin"
  member  = "serviceAccount:${data.google_project.current.number}-compute@developer.gserviceaccount.com"
}