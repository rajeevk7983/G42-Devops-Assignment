# start by pulling the python image
# FROM python:3.8-alpine
FROM centos:latest

RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
RUN yum update -y
RUN yum install wget redhat-lsb-core python3-pip python3 git -y

# copy the requirements file into the image
COPY ./required-moldules-list.txt /application/required-moldules-list.txt

# switch working directory
WORKDIR /application

# install the dependencies and packages in the requirements file
RUN pip install -r required-moldules-list.txt

# copy every content from the local file to the image
COPY . /application

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["main.py" ]
