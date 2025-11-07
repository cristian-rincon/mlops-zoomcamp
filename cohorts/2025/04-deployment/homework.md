## Homework

In this homework, we'll deploy the ride duration model in batch mode. Like in homework 1, we'll use the Yellow Taxi Trip Records dataset. 

You'll find the starter code in the [homework](homework) directory.

Solution: [homework_solution/](homework_solution/)


## Q1. Notebook

We'll start with the same notebook we ended up with in homework 1.
We cleaned it a little bit and kept only the scoring part. You can find the initial notebook [here](homework/starter.ipynb).

Run this notebook for the March 2023 data.

What's the standard deviation of the predicted duration for this dataset?

* 1.24
* [x] 6.24
* 12.28
* 18.28


## Q2. Preparing the output

Like in the course videos, we want to prepare the dataframe with the output. 

First, let's create an artificial `ride_id` column:

```python
df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
```

Next, write the ride id and the predictions to a dataframe with results. 

Save it as parquet:

```python
df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)
```

What's the size of the output file?

* 36M
* 46M
* 56M
* [x] 60M
* 66M

__Note:__ Make sure you use the snippet above for saving the file. It should contain only these two columns. For this question, don't change the
dtypes of the columns and use `pyarrow`, not `fastparquet`. 


## Q3. Creating the scoring script

Now let's turn the notebook into a script. 

Which command you need to execute for that?

```bash
uv run -- jupyter nbconvert starter.ipynb --to script

-- Output
(2025) ➜  homework git:(04-deployment) ✗ uv run -- jupyter nbconvert starter.ipynb --to script
[NbConvertApp] Converting notebook starter.ipynb to script
[NbConvertApp] Writing 2073 bytes to starter.py
```


## Q4. Virtual environment

Now let's put everything into a virtual environment. We'll use pipenv for that.

Install all the required libraries. Pay attention to the Scikit-Learn version: it should be the same as in the starter
notebook.

After installing the libraries, pipenv creates two files: `Pipfile`
and `Pipfile.lock`. The `Pipfile.lock` file keeps the hashes of the
dependencies we use for the virtual env.

What's the first hash for the Scikit-Learn dependency?

R:
```toml
sdist = { url = "https://files.pythonhosted.org/packages/bf/8a/06e499bca463905000f50e461c9445e949aafdd33ea3b62024aa2238b83d/scikit_learn-1.5.0.tar.gz", hash = "sha256:789e3db01c750ed6d496fa2db7d50637857b451e57bcae863bff707c1247bef7", size = 7820839, upload-time = "2024-05-21T16:34:07.711Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/1e/21/fe8e90eb7dc796ed384daaf45a83e729a41fa7a9bf14bc1a0b69fd05b39a/scikit_learn-1.5.0-cp312-cp312-macosx_10_9_x86_64.whl", hash = "sha256:460806030c666addee1f074788b3978329a5bfdc9b7d63e7aad3f6d45c67a210", size = 12096541, upload-time = "2024-05-21T16:33:36.475Z" },
    { url = "https://files.pythonhosted.org/packages/f9/4b/c035ce6771dd56283cd587e941054ebb38a14868729e28a0f7c6c9ff9ebd/scikit_learn-1.5.0-cp312-cp312-macosx_12_0_arm64.whl", hash = "sha256:1b94d6440603752b27842eda97f6395f570941857456c606eb1d638efdb38184", size = 11031507, upload-time = "2024-05-21T16:33:39.896Z" },
    { url = "https://files.pythonhosted.org/packages/66/a1/e64f125382f2fc46dd1f3a3c2d390f02db896e3803a3e7898c4ca48390e0/scikit_learn-1.5.0-cp312-cp312-manylinux_2_17_aarch64.manylinux2014_aarch64.whl", hash = "sha256:d82c2e573f0f2f2f0be897e7a31fcf4e73869247738ab8c3ce7245549af58ab8", size = 12082985, upload-time = "2024-05-21T16:33:42.807Z" },
    { url = "https://files.pythonhosted.org/packages/ae/54/e70102a9c12d27d985ba659f336851732415e5a02864bef2ead36afaf15d/scikit_learn-1.5.0-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl", hash = "sha256:a3a10e1d9e834e84d05e468ec501a356226338778769317ee0b84043c0d8fb06", size = 13065320, upload-time = "2024-05-21T16:33:45.65Z" },
    { url = "https://files.pythonhosted.org/packages/57/ed/f607ebf69f87bcce2e3fa329bd78da8cafd3d51190a19d58012d2d7f2252/scikit_learn-1.5.0-cp312-cp312-win_amd64.whl", hash = "sha256:855fc5fa8ed9e4f08291203af3d3e5fbdc4737bd617a371559aaa2088166046e", size = 10938084, upload-time = "2024-05-21T16:33:49.011Z" },
]
```

## Q5. Parametrize the script

Let's now make the script configurable via CLI. We'll create two 
parameters: year and month.

Run the script for April 2023. 

What's the mean predicted duration? 

* 7.29
* [x] 14.29
* 21.29
* 28.29

Hint: just add a print statement to your script.


## Q6. Docker container 

Finally, we'll package the script in the docker container. 
For that, you'll need to use a base image that we prepared. 

This is what the content of this image is:

```dockerfile
FROM python:3.10.13-slim

WORKDIR /app
COPY [ "model2.bin", "model.bin" ]
```

Note: you don't need to run it. We have already done it.

It is pushed to [`agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim`](https://hub.docker.com/layers/agrigorev/zoomcamp-model/mlops-2024-3.10.13-slim/images/sha256-f54535b73a8c3ef91967d5588de57d4e251b22addcbbfb6e71304a91c1c7027f?context=repo),
which you need to use as your base image.

That is, your Dockerfile should start with:

```dockerfile
FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

# do stuff here
```

This image already has a pickle file with a dictionary vectorizer
and a model. You will need to use them.

Important: don't copy the model to the docker image. You will need
to use the pickle file already in the image. 

Now run the script with docker. What's the mean predicted duration
for May 2023? 

* 0.19
* 7.24
* [x] 14.24
* 21.19


## Bonus: upload the result to the cloud (Not graded)

Just printing the mean duration inside the docker image 
doesn't seem very practical. Typically, after creating the output 
file, we upload it to the cloud storage.

Modify your code to upload the parquet file to S3/GCS/etc.


## Bonus: Use an orchestrator for batch inference

Here we didn't use any orchestration. In practice we usually do.

* Split the code into logical code blocks
* Use a workflow orchestrator for the code execution

## Publishing the image to dockerhub

This is how we published the image to Docker hub:

```bash
docker build -t mlops-zoomcamp-model:2024-3.10.13-slim .
docker tag mlops-zoomcamp-model:2024-3.10.13-slim agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

docker login --username USERNAME
docker push agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim
```

This is just for your reference, you don't need to do it.


## Submit the results

* Submit your results here: https://courses.datatalks.club/mlops-zoomcamp-2025/homework/hw4
* It's possible that your answers won't match exactly. If it's the case, select the closest one.
