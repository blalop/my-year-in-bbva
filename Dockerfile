FROM python:3.10-slim

WORKDIR /yearinbbva

VOLUME db
ENV MYYEARINBBVA_PATH /db/movements.db
ENV HOST 0.0.0.0

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY yearinbbva yearinbbva

CMD ["python", "yearinbbva"]
