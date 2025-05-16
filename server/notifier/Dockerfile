# Use official Miniconda3 image as base
FROM continuumio/miniconda3:latest

# Set working directory
WORKDIR /app

# Copy environment.yml and install dependencies
COPY environment.yml .
RUN conda env create -f environment.yml

# Make sure conda environment is activated:
SHELL ["conda", "run", "-n", "doorbell-notifier", "/bin/bash", "-c"]

# Copy the application code
COPY mqtt_to_pushbullet.py .
COPY config/settings.json ./config/settings.json
COPY start.sh .
RUN chmod +x start.sh

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["./start.sh"]