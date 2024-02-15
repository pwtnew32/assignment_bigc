# defind master image
# FROM apache/airflow:2.7.0

FROM apache/airflow:2.7.0
# copy local connector into container
COPY requirement.txt /requirement.txt

# upgrade pip
RUN python -m pip install --upgrade pip
# run pip install
RUN pip install --requirement /requirement.txt
