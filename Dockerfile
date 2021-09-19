FROM rasa/rasa-sdk:2.8.2

USER root

RUN apt update && \
    apt install -y git \
        make
        
RUN pip install black \
    ray[default]==1.6.0