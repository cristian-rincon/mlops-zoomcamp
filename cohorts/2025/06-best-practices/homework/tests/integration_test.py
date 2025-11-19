import os
import pandas as pd
from datetime import datetime

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

def main():
    # Set up environment variables
    os.environ['INPUT_FILE_PATTERN'] = "s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
    os.environ['OUTPUT_FILE_PATTERN'] = "s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
    os.environ['S3_ENDPOINT_URL'] = "http://localhost:4566"

    # Create test data
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df_input = pd.DataFrame(data, columns=columns)

    # Save to S3
    input_file = os.environ['INPUT_FILE_PATTERN'].format(year=2023, month=1)
    options = {
        'client_kwargs': {
            'endpoint_url': os.environ['S3_ENDPOINT_URL']
        }
    }
    
    df_input.to_parquet(
        input_file,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options
    )

    print(f"Created input file: {input_file}")

    # Run batch.py
    os.system('python batch.py 2023 1')

    # Verify result
    output_file = os.environ['OUTPUT_FILE_PATTERN'].format(year=2023, month=1)
    df_result = pd.read_parquet(output_file, storage_options=options)

    print("Result dataframe:")
    print(df_result)
    
    print(f"Sum of predicted durations: {df_result['predicted_duration'].sum()}")

if __name__ == '__main__':
    main()
