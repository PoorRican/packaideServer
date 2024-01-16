# Running

## Using Docker

The Docker container is a pain-free way of running this server as it can be run locally or on a server.
The Docker installation instructions may be found [here](https://docs.docker.com/engine/install/)

Once Docker is installed, the container is built with the following command. This step only needs to be completed once.
```bash
docker build -t packaide_server .
```

To run the container in the background, use the following command:
```bash
docker run -d packaide_server
```

## Local Installation

While a Docker container will be made available, running the FastAPI server locally requires that [Packaide (v2 branch)](https://github.com/DanielLiamAnderson/Packaide/tree/v2)
be installed. Follow the instructions provided in the [Packaide README](https://github.com/DanielLiamAnderson/Packaide/tree/v2?tab=readme-ov-file#requirements)
to install locally.

To run locally, clone this repository and run the following commands:

Install requirements
```bash
pip install -r requirements.txt
```

Then to run the server itself, run the following command:
```bash
uvicorn main:app --reload
```