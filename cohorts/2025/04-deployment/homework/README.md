# Taxi Trip Prediction Model Container
This container provides a command-line interface (CLI) for making predictions using a pre-trained model for taxi trips. The model is designed to estimate outcomes (such as trip duration, fare, etc.) based on the specified year and month.

## Purpose
This project packages a machine learning model for taxi trip predictions into a portable Docker container. Users can easily run predictions by providing the year and month as parameters to the CLI tool inside the container.

## Getting Started
1. Pull the Image
Pull the latest image from Docker Hub:
```bash
docker pull crincon/zoomcamp-model:latest
```
Or, if you use Podman:
```bash    
podman pull crincon/zoomcamp-model:latest
```
2. Run the Container
To run a prediction, use the following command format:

```bash
docker run --rm crincon/zoomcamp-model:latest YEAR MONTH
```
Replace YEAR and MONTH with the desired values.
For example, to run a prediction for April 2023:

```bash
docker run --rm crincon/zoomcamp-model:latest 2023 4
```
If you use Podman, the command is the same:
```bash
podman run --rm crincon/zoomcamp-model:latest 2023 4
```

3. CLI Parameters
YEAR: The year for which you want to make a prediction (e.g., 2023)
MONTH: The month for which you want to make a prediction (e.g., 4 for April)
4. Example Output
The CLI will output the prediction result directly to your terminal.

## Advanced Usage
If you want to use the Typer CLI directly (for example, to see help or other commands):
```
bash
docker run --rm crincon/zoomcamp-model:latest --help
```
### Notes
The container includes all necessary dependencies and the trained model.
No additional setup is required.
For questions or issues, please open an issue in the repository or contact the maintainer.
