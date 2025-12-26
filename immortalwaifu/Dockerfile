FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl wkhtmltopdf libxrender1 libxext6 fontconfig && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip setuptools

# ✅ requirements.txt same folder me hai
COPY requirements.txt /app/

RUN pip3 install --no-cache-dir -U -r requirements.txt

# ✅ Copy rest of the code
COPY . /app/

CMD ["python", "-m", "bot"]
