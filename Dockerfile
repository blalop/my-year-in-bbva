FROM python:3.10-slim

VOLUME documents
ENV DIRECTORY documents

COPY requirements.txt .
RUN apt-get update && apt-get install build-essential libpoppler-cpp-dev pkg-config python3-dev -y --no-install-recommends
RUN pip3 install -r requirements.txt

COPY yearinbbva/ /yearinbbva

CMD ["python", "yearinbbva"]
