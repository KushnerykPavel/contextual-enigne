FROM golang:1.21 as build

WORKDIR /app

COPY . .
RUN make build

WORKDIR /app/bin

CMD ["./main"]