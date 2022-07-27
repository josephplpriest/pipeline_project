FROM python:3.10


WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install --upgrade pip

RUN python3 -m venv venv

SHELL ["/bin/bash", "-c"] 

RUN source venv/bin/activate

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

RUN pytest

CMD ["python", "scraper_main.py"]