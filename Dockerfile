FROM python:3.10-slim-buster

WORKDIR /app

COPY libraryrequirements.txt .  # Copy the requirements file into the container

RUN pip install --upgrade pip  # Upgrade pip to the latest version

RUN pip install -r libraryrequirements.txt  # Install dependencies from the requirements file

COPY . .  # Copy all the application files into the container

EXPOSE 8000  # Expose the port that the app will run on

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]  # Run the FastAPI app with uvicorn
