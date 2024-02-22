FROM python:3.9-slim
COPY . .
RUN pip3 install -q -r requirements.txt
CMD [ "python", "main.py"]