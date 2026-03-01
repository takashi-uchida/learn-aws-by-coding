FROM python:3.12-slim

ENV HOME /root

# Install pytorch (CPU only)
RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install other python libraries
RUN pip3 install \
    boto3

COPY main.py model.py ${HOME}/

WORKDIR ${HOME}
ENTRYPOINT ["python3", "main.py"]
