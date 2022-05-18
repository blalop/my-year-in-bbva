FROM python:3.9

VOLUME documents

COPY requirements.txt .
RUN apt-get update && apt-get install libpoppler-cpp-dev -y --no-install-recommends
RUN pip3 install -r requirements.txt

COPY yearinbbva/ /yearinbbva

CMD ["python", "yearinbbva"]
