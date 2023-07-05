# Date Engineering Pipeline project - Temperature - Energy Consumption

This project combines Terraform infrastructure as code and a Python script to extract data from a raw dataset, transform it into appropriate columns, and upload it to Google Cloud Platform (GCP) BigQuery. The Terraform code automates the creation of BigQuery resources and a Dataflow job, while the Python script handles the data extraction and transformation process.


## Prerequisites
Before using this project, ensure that you have the following prerequisites:

**Google Cloud Platform (GCP) Account**: You need a GCP account with appropriate permissions to create BigQuery resources and Dataflow jobs.
**Terraform**: Install Terraform on your local machine to execute the Terraform code.
**Python**: Ensure that Python is installed on your local machine. The script relies on Python to perform the data extraction and transformation.

## Running Local Test

Run the following command to execute the Python script locally:

```sh
python temperature_processing.py \
--project <your-project-id> \
--region <desired-region> \
--dataset_id <desired-dataset-id> \
--table_id <desired-table-id> \
--template_location gs://<bucket-name>/template-file/temperature-preprocessing.json \
--temp_location gs://<bucket-name>/temp \
--raw_data_bucket gs://<raw-data-bucket-name>

```

Replace the placeholders `<your-project-id>`, `<desired-region>`, `<desired-dataset-id>`, `<desired-table-id>`, `<bucket-name>`, and `<raw-data-bucket-name>` with your actual values.

The command will initiate the execution of the Python script locally, simulating the data processing flow. The script will read the sample raw data file located at `gs://<raw-data-bucket-name>` and perform the necessary data extraction and transformation steps.

The processed data will be written to the specified `<desired-dataset-id>`.`<desired-table-id>` in the BigQuery dataset.

## Creating Dataflow Template

To create a Dataflow template based on the provided Python code, follow the steps below:

Run the following command to generate the Dataflow template:

```sh
python temperature_processing.py \
--runner DataflowRunner \
--project <your-project-id> \
--region <desired-region> \
--temp_location gs://<bucket-name>/template-file/temp \
--staging_location gs://<bucket-name>/template-file/staging \
--template_location gs://<bucket-name>/template-file/temperature-preprocessing.json \
--dataset_id <desired-dataset-id> \
--table_id <desired-table-id> \
--raw_data_bucket gs://<raw-data-bucket-name>

```

Replace the placeholders `<your-project-id>`, `<desired-region>`, `<bucket-name>`, `<desired-dataset-id>`, `<desired-table-id>`, and `<raw-data-bucket-name>` with your actual values.

The command will initiate the execution of the Python script in DataflowRunner mode, generating a template file (`temperature-preprocessing.json`) in the specified Cloud Storage location.

Once the command completes successfully, you will find the generated Dataflow template at the specified Cloud Storage location (`gs://<bucket-name>/template-file/temperature-preprocessing.json`).

The Dataflow template can now be used with Terraform or directly in the GCP Console to create and execute Dataflow jobs based on the provided Python code.

# Terraform

## Providers

| Name | Version |
|------|---------|
| <a name="provider_google"></a> [google](#provider\_google) | n/a |

## Resources

| Name | Type |
|------|------|
| [google_bigquery_dataset.dataset](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset) | resource |
| [google_bigquery_table.table](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_table) | resource |
| [google_dataflow_job.dataflow](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/dataflow_job) | resource |
| [google_project_iam_member.compute_engine_service_account](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/project_iam_member) | resource |
| [google_project_iam_member.dataflow_admin](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/project_iam_member) | resource |
| [google_storage_bucket.backend_bucket](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket) | resource |
| [google_storage_bucket.raw_data_bucket](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket) | resource |
| [google_storage_bucket.various_files](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket) | resource |
| [google_storage_bucket_object.requirements](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket_object) | resource |
| [google_project.current](https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/project) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_dataset_id"></a> [dataset\_id](#input\_dataset\_id) | n/a | `string` | `"temperature"` | no |
| <a name="input_files_bucket_name"></a> [files\_bucket\_name](#input\_files\_bucket\_name) | Variable for generic bucket | `string` | `"generic-files-123456789"` | no |
| <a name="input_project_id"></a> [project\_id](#input\_project\_id) | n/a | `string` | `"cr-lab-pedouard-123456789"` | no |
| <a name="input_region"></a> [region](#input\_region) | n/a | `string` | `"europe-west1"` | no |
| <a name="input_table_id"></a> [table\_id](#input\_table\_id) | n/a | `string` | `"temperature"` | no |
| <a name="input_template_file_name"></a> [template\_file\_name](#input\_template\_file\_name) | n/a | `string` | `"temperature-preprocessing"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_dataset_id"></a> [dataset\_id](#output\_dataset\_id) | n/a |
| <a name="output_raw_data_bucket_name"></a> [raw\_data\_bucket\_name](#output\_raw\_data\_bucket\_name) | Outputs the name of the new bucket for raw data |
| <a name="output_service_account_email"></a> [service\_account\_email](#output\_service\_account\_email) | n/a |
| <a name="output_table_id"></a> [table\_id](#output\_table\_id) | n/a |
<!-- END_TF_DOCS -->