# Build
FROM maven:3.9.7-sapmachine-22 AS build

COPY src /home/app/src
COPY src/main/resources/application-prod.properties /home/app/src/main/resources/application.properties
COPY pom.xml /home/app
RUN mvn -q -f /home/app/pom.xml clean package

# Production
FROM openjdk:22

COPY --from=build /home/app/target/*.jar /app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app.jar"]