FROM python:3.10.6

ENV PYTHONUNBUFFERED=1

WORKDIR /Blog-site

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
