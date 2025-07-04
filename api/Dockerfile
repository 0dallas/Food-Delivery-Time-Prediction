FROM python:3.10-slim-buster

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for models inside the app folder
RUN mkdir -p /app/models

# Copy the preprocessor and model artifacts into the /app/models directory
COPY models/model.pkl /app/models/
COPY models/preprocessor.pkl /app/models/

# Copy the application code 
COPY app/ /app/app/

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]