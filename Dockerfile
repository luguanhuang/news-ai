FROM ubuntu:22.04
#定义时区参数
ENV TZ=Asia/Shanghai
#设置时区
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo '$TZ' > /etc/timezone
#设置编码
ENV LANG C.UTF-8
RUN sed -i 's/archive.ubuntu.com/mirrors.tencent.com/g' /etc/apt/sources.list
RUN sed -i 's/security.ubuntu.com/mirrors.tencent.com/g' /etc/apt/sources.list

# RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
# RUN sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN mkdir -p /code
RUN mkdir -p /data
WORKDIR /code
COPY . .
RUN ls -a /code

RUN apt update -y && apt install python3-pip pkg-config python3-dev default-libmysqlclient-dev build-essential -y

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

WORKDIR /code/
ENV PYTHONPATH "${PYTONPATH}:/code/"
CMD ["/bin/bash","/code/run.sh"]