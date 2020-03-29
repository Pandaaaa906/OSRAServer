FROM python:3.6 AS builder

#COPY imago/imago_console /opt

COPY . /osra_server
WORKDIR /osra_server

RUN chmod 777 /osra_server/imago/imago_console

RUN mkdir ~/.pip
RUN echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" | tee ~/.pip/pip.conf
RUN pip install -r requirements

FROM builder AS runner

CMD python3 main.py

EXPOSE 9191