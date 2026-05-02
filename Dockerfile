FROM quay.io/astronomer/astro-runtime:3.2-2

USER root

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libnss3 \
    libxi6 \
    libxrender1 \
    libxtst6 \
    libxss1 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    fonts-liberation \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER astro
