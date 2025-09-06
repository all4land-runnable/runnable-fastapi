FROM ubuntu:latest
LABEL authors="kmj"

ENTRYPOINT ["top", "-b"]