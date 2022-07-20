FROM python:3.10

COPY requirements.txt ./

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . .

RUN pytest

CMD ["python", "scraper_main.py"]