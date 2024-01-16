FROM archlinux

# Install dependencies
RUN pacman -Sy --noconfirm git python python-pip python-virtualenv clang cmake cgal

# Setup virtualenv
# There is a more elegant way to set up the virtualenv as per https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/opt/venv
RUN python -m virtualenv ${VIRTUAL_ENV}

# Install packaide
RUN git clone https://github.com/DanielLiamAnderson/Packaide /opt/Packaide/
RUN cd /opt/Packaide && \
    git checkout v2 && \
    ${VIRTUAL_ENV}/bin/pip install -r requirements.txt && \
    ${VIRTUAL_ENV}/bin/pip install .

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
CMD ["/opt/venv/bin/python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]