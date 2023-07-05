import sys
import time
import argparse
import apache_beam as beam
from google.cloud import bigquery
from apache_beam.options.pipeline_options import PipelineOptions

def collectArguments():
    # Define the required arguments for data processing mode
    required_arguments = ['project', 'dataset_id', 'table_id', 'raw_data_bucket']

    # Create the argument parser
    parser = argparse.ArgumentParser()

    # Add the required arguments for data processing mode
    for arg in required_arguments:
        parser.add_argument('--' + arg, required=True, help=arg + ' is a required argument')

    # Parse the command-line arguments
    args, _ = parser.parse_known_args()

    # Check if all required arguments are present for data processing mode
    missing_arguments = [arg for arg in required_arguments if not getattr(args, arg)]
    if missing_arguments:
        print('The following required arguments are missing:', ', '.join(missing_arguments))
        sys.exit(1)

    return args

# Create a dict to store data in BigQuery format
bigquery_schema = {
    'fields': [
        {'name': 'station_code',        'type': 'STRING'},
        {'name': 'month',               'type': 'STRING'},
        {'name': 'average_temperature', 'type': 'FLOAT'},
        {'name': 'latitude',            'type': 'FLOAT'},
        {'name': 'longitude',           'type': 'FLOAT'}
    ]
}

# Assign argument values to variables
arguments = collectArguments()
project = arguments.project
dataset_id = arguments.dataset_id
table_id = arguments.table_id
raw_data_bucket = arguments.raw_data_bucket

class ProcessingTemperature(beam.DoFn):

    months = {
        '01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December'
    }

    def process(self, element, side_input):
        # Split the CSV row by commas
        fields = element.split(',')

        # Extract the desired data fields
        try:
            station_code = fields[0]
            month = self.months[fields[1][4:6]]
            measurement_type = fields[2]
            measurement_value = fields[3]
        except IndexError:
            print("IndexError while processing row:" + element)

        if measurement_type == "TAVG":
            # Extract the latitude and longitude from the station information
            # Search for a matching station from the side input
            matching_station = None

            for station in side_input:
                try:
                    if station['station_code'] == station_code:
                        matching_station = station
                        break
                except TypeError:
                    print(f'Error with station code: {station_code}')

            # Format data into dict for BigQuery
            formatted_data = {
                "station_code": station_code,
                "month": month,
                "average_temperature": measurement_value,
                "latitude": matching_station['latitude'] if matching_station is not None else 0.0,
                "longitude": matching_station['longitude'] if matching_station is not None else 0.0
            }

            # Yield the data
            yield formatted_data

def process_side_input(element):
    station_code = element[0:11].strip()
    latitude = float(element[12:20].strip())
    longitude = float(element[21:30].strip())
    elevation = float(element[31:38].strip())
    location = element[39:71].strip()

    return {
        'station_code': station_code,
        'latitude': latitude,
        'longitude': longitude,
        'elevation': elevation,
        'location': location
    }

def run_pipeline():
    # Create the pipeline with the specified options
    # options = beam.options.pipeline_options.PipelineOptions()
    options = PipelineOptions()
    with beam.Pipeline(options=options) as pipeline:
        # Read input data from file in GCP Storage
        input_files = f'gs://{raw_data_bucket}/sample_2015.csv'

        # Handle data processing mode logic
        print('Running in data processing mode...')

        # [Output PCollection] = [Input PCollection] | [Name String] >> [Transform]

        # Read multiple CSV files
        temperature_data_PCol = pipeline | 'Read Temperature CSV Data' >> beam.io.ReadFromText(input_files)

        # Read the side input data
        side_input_file = f'gs://{raw_data_bucket}/sample-ghcnd-stations.txt'

        # Process the side input data
        side_input_PCol = (pipeline
                            | 'Read Stations Side Input' >> beam.io.ReadFromText(side_input_file)
                            | 'Process Stations Side Input' >> beam.Map(process_side_input))

        # Apply the ParDo transform to extract the temperature data
        extracted_data_PCol = temperature_data_PCol | 'Process Temperature Data' >> beam.ParDo(ProcessingTemperature(), side_input=beam.pvalue.AsList(side_input_PCol))

        # Load the extracted dict data into BigQuery
        load_to_bigquery = (
            extracted_data_PCol
            | "Write to BigQuery" >> beam.io.WriteToBigQuery(
                table=table_id,
                dataset=dataset_id,
                project=project,
                schema=bigquery_schema,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )

        # Run the pipeline
        result = pipeline.run()

if __name__ == "__main__":
    run_pipeline()