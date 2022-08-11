# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./required-moldules-list.txt /app/required-moldules-list.txt

# switch working directory
WORKDIR /application

# install the dependencies and packages in the requirements file
RUN pip install -r required-moldules-list.txt

# copy every content from the local file to the image
COPY . /application

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["main.py" ]