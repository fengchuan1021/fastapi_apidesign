FROM python:3.10
WORKDIR /app
RUN  apt-get clean
RUN apt-get update
ENV DEBIAN_FRONTEND noninteractive

RUN /bin/cp /usr/share/zoneinfo/Europe/London /etc/localtime && echo 'Europe/London' >/etc/timezone
COPY requirements.txt /etc/requirements.txt
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /etc/requirements.txt
COPY patch.py /app/patch.py
COPY patchs/ /app/patchs/
RUN python patch.py
COPY . /app
CMD sh ./dockerstart.sh