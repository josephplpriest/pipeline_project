FROM python:3.10

WORKDIR /streamlit

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip

RUN python3 -m venv venv

SHELL ["/bin/bash", "-c"] 

RUN mkdir data

RUN source venv/bin/activate

RUN pip3 install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py"]