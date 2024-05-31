FROM python:3.10-bookworm

# Install dependencies
RUN pip install virtualenv
RUN apt-get update
RUN apt-get install git libcgal-dev -y

# Setup virtualenv
# There is a more elegant way to set up the virtualenv as per https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/opt/venv
RUN virtualenv ${VIRTUAL_ENV}

# Install packaide
RUN git clone https://github.com/DanielLiamAnderson/Packaide /opt/Packaide/
RUN cd /opt/Packaide && \
    git checkout v2 && \
    ${VIRTUAL_ENV}/bin/pip install -r requirements.txt && \
    ${VIRTUAL_ENV}/bin/pip install .

# Remove unnecessary files
RUN rm -rf /opt/Packaide
RUN apt-get remove git clang cmake -y

# Setup server
ENV DIR=/opt/packaideServer

RUN mkdir ${DIR}
RUN cd ${DIR}
COPY ./requirements.txt ${DIR}/requirements.txt

RUN ${VIRTUAL_ENV}/bin/pip install -r ${DIR}/requirements.txt

# Copy over server files
COPY ./main.py ${DIR}
COPY ./utils.py ${DIR}

WORKDIR ${DIR}
EXPOSE 8000
CMD ["/opt/venv/bin/python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]