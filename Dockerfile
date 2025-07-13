#base image 
FROM nvidia/cuda:12.2.0-base-ubuntu20.04

#set env variables
# Don't generate .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 
  # Ensure stdout is flushed 
ENV PYTHONUNBUFFERED=1       
ENV DEBIAN_FRONTEND=noninteractive

#set working dir
WORKDIR /app

#install system packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    wget \
    curl \
    && apt-get clean

#create sym;ink for python command
RUN ln -s /usr/bin/python3 /usr/bin/python

#upgrade pip and install python packages 
COPY requirements.txt . 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 

#copy project files into container
COPY . .

#expose port for FASTAPI
EXPOSE 8000

#default command 
CMD ["uvicorn", "controllers.agent_orchestrator:app", "--host", "0.0.0.0", "--port", "8000"]

