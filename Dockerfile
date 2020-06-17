FROM archlinux
MAINTAINER Oluwaseun Peter "adepeter26@gmail.com"
LABEL version="0.0.1"
LABEL location="Sokoto, Nigeria"
RUN pacman -Syy --noconfirm
RUN pacman -S python python-pipenv python-django --noconfirm
RUN pacman -Scc --noconfirm
SHELL ["bin/bash"]
CMD ["bin/bash"]
EXPOSE 8000