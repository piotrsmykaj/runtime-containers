RUN apt-get update && apt-get install -y --no-install-recommends \
    python-pip python-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install awscli
