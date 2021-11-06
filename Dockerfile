FROM continuumio/miniconda3

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . $APP_HOME

# RUN apk update
# RUN apk install espeak 
# RUN apk add build-base
# RUN apk install gcc

#---------------- Prepare the envirennment
RUN conda install -c conda-forge pyaudio
RUN pip install -r REQUIREMENTS.txt

SHELL ["conda", "run", "--name", "app", "/bin/bash", "-c"]
CMD ["python", "api.py"]

