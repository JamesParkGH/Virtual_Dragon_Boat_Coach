FROM continuumio/miniconda3

WORKDIR /app/src

COPY src /app/src
COPY requirements.txt /app/src/requirements.txt

# Create Conda environment & install dependencies
RUN conda create -n myenv python=3.11 -y
RUN echo "conda activate myenv" >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc && conda install -y -c opensim-org opensim && pip install -r requirements.txt"

# Start the app with Conda
CMD ["/bin/bash", "-c", "source ~/.bashrc && gunicorn app:app"]