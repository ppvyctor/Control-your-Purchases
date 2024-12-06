FROM python:3.12.3

WORKDIR /app

COPY Product_Purchases.py /app

RUN pip install regex
RUN pip install pandas
RUN pip install numpy
RUN pip install openpyxl
RUN pip install mysql-connector-python

EXPOSE 8501

CMD ["streamlit", "run", "Product_Purchases.py", "--server.port=8501", "--server.enableCORS=false"]