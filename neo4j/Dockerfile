FROM neo4j:latest

COPY constraints.sh ./
COPY wrapper.sh ./

RUN chmod +x ./constraints.sh
RUN chmod +x ./wrapper.sh

ENTRYPOINT ["./wrapper.sh"]