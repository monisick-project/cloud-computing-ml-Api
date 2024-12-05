FROM python:3.10-slim-buster

WORKDIR /app

<<<<<<< HEAD
COPY libraryrequirement.txt .  

RUN pip install --no-cache-dir -r libraryrequirement.txt  

COPY . .  

EXPOSE 8000  

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]  
=======
COPY libraryrequirement.txt . 

RUN pip install --upgrade pip  

RUN pip install -r libraryrequirement.txt  

COPY . .  

EXPOSE 8000  

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]  
>>>>>>> 735c7ccdca277d14cfaf079fc3ff8e3e998d4ed9
