# Setup bigquery on GCP
resource "google_bigquery_dataset" "dataset" {
  dataset_id    = var.dataset_id
  friendly_name = "Average Temperature Dataset"
  description   = "The Average Temperature dataset including station code"
  location      = "EU"
}

# BigQuery - Schema
# {
#     "type": "record",
#     "name": "TemperatureData",
#     "fields": [
#         {"name": "station_code", "type": "string"},
#         {"name": "month", "type": "string"},
#         {"name": "average_temperature", "type": "float"},
#         {"name": "latitude", "type": "float"},
#         {"name": "longitude", "type": "float"}
#     ]
# }

resource "google_bigquery_table" "table" {
  dataset_id          = google_bigquery_dataset.dataset.dataset_id
  table_id            = var.table_id
  deletion_protection = false
  schema              = <<EOF
[
  {
    "name": "station_code",
    "type": "STRING"
  },
  {
    "name": "month",
    "type": "STRING"
  },
  {
    "name": "average_temperature",
    "type": "FLOAT"
  },
  {
    "name": "latitude",
    "type": "FLOAT"
  },
  {
    "name": "longitude",
    "type": "FLOAT"
  }
]
EOF
}