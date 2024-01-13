FROM python:3.12

# Install dependencies
RUN apt-get update && apt-get install -y git libcgal-dev

# install packaide
RUN git clone https://github.com/DanielLiamAnderson/Packaide /tmp/Packaide/

RUN cd /tmp/Packaide
RUN git checkout v2
RUN pip install --user . -r requirements.txt

# setup server
ENV DIR=/opt/packaideServer

RUN mkdir ${DIR}
RUN cd ${DIR}
COPY ./requirements.txt ${DIR}/requirements.txt

RUN pip install --no-cache-dir --upgrade -r ${DIR}/requirements.txt

# Copy over server files
COPY ./main.py ${DIR}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]