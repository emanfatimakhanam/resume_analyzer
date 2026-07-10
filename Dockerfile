FROM python:3.11-slim

# Install system-level dependencies: Tesseract OCR and Poppler
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir spacy scikit-learn
RUN python -m spacy download en_core_web_sm

COPY . .

# On Linux, Tesseract and Poppler are installed system-wide and found via PATH automatically —
# TESSERACT_PATH / POPPLER_PATH env vars are not needed the way they were on Windows.
ENV TESSERACT_PATH=/usr/bin/tesseract
ENV POPPLER_PATH=/usr/bin

CMD gunicorn --bind 0.0.0.0:$PORT app:app