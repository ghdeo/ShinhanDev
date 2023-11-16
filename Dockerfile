FROM golang:1.20.1-alpine3.17 AS builder
WORKDIR /work
COPY . /work/
RUN go build -o server main.go

FROM alpine:3.14
COPY --from=builder /work/server /work/server
ENTRYPOINT ["/work/server"]
