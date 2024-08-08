FROM python:3.12.4-alpine3.20

WORKDIR /app

COPY requirements.txt ./
RUN pip install pip --upgrade -v
RUN pip install --no-cache-dir -r requirements.txt

COPY ../ /app

# https://gitlab.alpinelinux.org/alpine/aports/-/issues/12057
ENV TZ="America/Caracas"
RUN apk add --no-cache tzdata
RUN ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime

EXPOSE 8000

CMD ["python", "app.py"]
