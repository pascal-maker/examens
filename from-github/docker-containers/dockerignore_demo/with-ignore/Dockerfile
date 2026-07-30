FROM alpine:3.20
WORKDIR /app
COPY . .
CMD ["sh", "-c", "echo 'Files copied into image:' && find /app -type f | sort"]
