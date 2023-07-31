FROM debian:bullseye

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y gnupg2 dirmngr

RUN echo "deb https://cloud.r-project.org/bin/linux/debian buster-cran40/" >> /etc/apt/sources.list

RUN gpg --keyserver keyserver.ubuntu.com --recv-keys E19F5F87128899B192B1A2C2AD5F960A256A04AF

RUN apt-get update && apt-get install -y r-base

RUN apt-get install -y vim curl python3 python3-dev python3-pip python3-venv

RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

RUN python3 -m pip install rpy2
RUN python3 -m pip install psutil
RUN python3 -m pip install plotly
RUN python3 -m pip install pandas


### test for crash in build if rpy2 and venv are not set up correctly
RUN python3 -c "from rpy2 import robjects as ro; print(ro.r('runif(10)'))"

RUN R -e "install.packages(c('data.table','lobstr'),dependencies=TRUE, repos='http://cran.rstudio.com/')" 

RUN mkdir -p /var/temp/
COPY ./gentest.py /var/temp/
COPY ./gentest.R /var/temp/
