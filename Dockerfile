FROM archlinux
MAINTAINER Oluwaseun Peter "adepeter26@mail.comcom"
LABEL version="0.0.1"
RUN pacman -Syu -y; pacman -Scc -y -y
RUN pacman -S python -y; pacman -S python-pipenv
ENV PROJECT_BASE_DIR /django
ENV PROJECT_WORK_DIR /$HOME/$PROJECT_BASE_DIR
RUN mkdir -p $PROJECT_WORK_DIR
WORKDIR $PROJECT_WORK_DIR
EXPOSE 8000