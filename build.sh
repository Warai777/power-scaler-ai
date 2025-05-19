#!/usr/bin/env bash
apt-get update && apt-get install -y wget unzip libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 libxss1 libgtk-3-0 libxshmfence1 libx11-xcb1

pip install -r requirements.txt
python -m playwright install chromium
