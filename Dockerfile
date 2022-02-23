FROM python

RUN pip install requests
RUN pip install bs4
RUN pip install argparse
RUN pip install lxml
COPY dsuc.py .
