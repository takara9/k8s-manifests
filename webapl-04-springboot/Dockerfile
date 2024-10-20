FROM maven:3.6.3-jdk-14 AS build
COPY src src
COPY pom.xml pom.xml
RUN  mvn clean package


FROM openjdk:8-jdk-alpine
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring

ARG JAR_FILE=target/*.jar
COPY --from=build ${JAR_FILE} app.jar
ENTRYPOINT ["java","-jar","/app.jar"]
