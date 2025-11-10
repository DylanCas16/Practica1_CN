FROM public.ecr.aws/lambda/python:3.12

WORKDIR /var/task

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY db_connection.py .
COPY db/ /var/task/db
COPY models/ /var/task/models

COPY lambda_functions/GetItems/getItems.py .

CMD [ "getItems.handler" ]