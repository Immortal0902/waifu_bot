FROM python:3.10-slim

WORKDIR /app

# System deps (safe ones)
RUN apt-get update && apt-get install -y \
    curl libxrender1 libxext6 fontconfig \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools

# requirements first (better caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy full project
COPY . .

# start bot
CMD ["python", "-m", "bot.main"]
