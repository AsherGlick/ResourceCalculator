FROM python:3.10-slim

WORKDIR /usr/src/app

RUN apt update && apt install -y python3 python3-pip pngquant npm

COPY . .

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY package.json ./
RUN npm install

# Full build (should always be uncommented when submitting a PR)
RUN [ "python", "./build.py" ]
# Draft build for faster testing, game can be changed in the 3rd arg (should always be commented out when submitting a PR)
# RUN [ "python", "./build.py", "The Forest", "--draft" ]

FROM httpd:2.4
COPY  --from=0 /usr/src/app/output/ /usr/local/apache2/htdocs/
