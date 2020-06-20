FROM archlinux
MAINTAINER Oluwaseun Peter "adepeter26@gmail.com"
LABEL version="0.0.1"
LABEL location="Sokoto, Nigeria"
RUN pacman -Syy --noconfirm && \
pacman -S python python-pipenv --noconfirm && \
pacman -Scc --noconfirm
COPY . home/sleekforum
RUN pip install --upgrade pip pipenv
WORKDIR home/sleekforum
EXPOSE 8000
#ENTRYPOINT ["python", "manage.py", "runserver"]
#CMD ["--settings=flyforum_project.settings.local"]