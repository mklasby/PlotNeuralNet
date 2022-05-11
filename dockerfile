FROM texlive/texlive:latest

LABEL maintainer = "Mike Lasby"
USER root

RUN apt-get update \
    && apt-get install -y python3 
# && apt-get install -y texlive-latex-base \
# && apt-get install -y texlive-fonts-recommended \
# && apt-get install -y texlive-fonts-extra \
# && apt-get install -y texlive-latex-extra

WORKDIR /workspace/plot-neural-net



