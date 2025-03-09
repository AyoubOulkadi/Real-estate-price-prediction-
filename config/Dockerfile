FROM python:3.10

# Mise à jour et installation des dépendances
RUN apt-get update && \
    mkdir -p /var/lib/apt/lists/partial && \
    apt install -y libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx && \
    apt install -y --force-yes \
        libu2f-udev fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 \
        libatspi2.0-0 libcairo2 libcups2 libdrm2 libgbm1 libgtk-3-0 libnspr4 \
        libnss3 libpango-1.0-0 libx11-6 libxcb1 libxcomposite1 libxdamage1 \
        libxext6 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils wget

# Télécharger et installer Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb || apt install -f -y && \
    rm google-chrome-stable_current_amd64.deb

# Vérifier que Google Chrome est installé correctement
RUN google-chrome --version

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY .. /app

CMD ["python", "-m", "src.data_collection.main"]
