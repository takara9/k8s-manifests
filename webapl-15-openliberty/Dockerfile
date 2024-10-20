FROM maven:3.6.3-jdk-14 AS build
COPY ./src /src
COPY ./pom.xml /pom.xml
RUN  mvn clean package

FROM openliberty/open-liberty:full-java11-openj9-ubi
ARG VERSION=1.0
ARG REVISION=SNAPSHOT
ENV default.http.port="9080"
ENV default.https.port="9443"
ENV app.context.root="/rest"

LABEL \
  org.opencontainers.image.authors="Your Name" \
  org.opencontainers.image.vendor="IBM" \
  org.opencontainers.image.url="local" \
  org.opencontainers.image.source="https://github.com/OpenLiberty/guide-getting-started" \
  org.opencontainers.image.version="$VERSION" \
  org.opencontainers.image.revision="$REVISION" \
  vendor="Open Liberty" \
  name="system" \
  version="$VERSION-$REVISION" \
  summary="The system microservice from the Getting Started guide" \
  description="This image contains the system microservice running with the Open Liberty runtime."

COPY --chown=1001:0 --from=build src/main/liberty/config/ /config/
COPY --chown=1001:0 --from=build target/*.war /config/apps/

RUN configure.sh
