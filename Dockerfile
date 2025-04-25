FROM jupyter/pyspark-notebook:latest

# Install any additional packages
RUN pip install --upgrade pip && \
    pip install findspark

EXPOSE 8888
