FROM python:2.7.15

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV TZ=Asia/Kolkata
CMD [ "python", "__init__.py" ]

