FROM archlinux
RUN pacman -Syy python python-pipenv --noconfirm && \
pacman -Scc --noconfirm
ENV BASE_DIR home
WORKDIR $BASE_DIR
RUN pip install --upgrade pip pipenv
SHELL ["bin/bash"]
RUN ["pipenv", "shell"]
ENV FORUM_PROJECT_DIR home/sleekforum
COPY . $FORUM_PROJECT_DIR
WORKDIR $FORUM_PROJECT_DIR
EXPOSE 8000
#ENTRYPOINT ["python", "manage.py", "runserver"]
#CMD ["--settings=flyforum_project.settings.local"]