FROM python:3.12

# Install dependencies
# cmake is not listed in the dependencies but is required for the install
RUN apt-get update && apt-get install -y git libcgal-dev cmake

# install packaide
RUN git clone https://github.com/DanielLiamAnderson/Packaide /tmp/Packaide/

RUN cd /tmp/Packaide && \
    git checkout v2 && \
    pip install -r requirements.txt && \
    pip install --user .

# setup server
ENV DIR=/opt/packaideServer

RUN mkdir ${DIR}
RUN cd ${DIR}
COPY ./requirements.txt ${DIR}/requirements.txt

RUN pip install --no-cache-dir --upgrade -r ${DIR}/requirements.txt

# Copy over server files
COPY ./main.py ${DIR}
COPY ./utils.py ${DIR}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]