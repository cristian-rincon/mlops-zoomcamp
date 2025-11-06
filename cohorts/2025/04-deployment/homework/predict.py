import pickle
import pandas as pd
import typer

app = typer.Typer()

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

@app.command()
def predict(year: int, month: int, model_path: str = "model.bin", output_file: str = "predictions.parquet"):
    # Load model and DictVectorizer
    with open(model_path, 'rb') as f_in:
        dv, model = pickle.load(f_in)

    data_url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    df = read_data(data_url)
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    # Print mean of predicted duration
    mean_pred = y_pred.mean()
    print(f"Mean predicted duration: {mean_pred:.2f}")

    # Prepare output
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    predictions_df = pd.DataFrame({
        'ride_id': df['ride_id'],
        'predicted_duration': y_pred
    })
    predictions_df.to_parquet(output_file, engine='pyarrow', compression=None, index=False)
    print(f"Predictions saved to {output_file}")

if __name__ == "__main__":
    app()