FROM archlinux
ARG user=sleekforum
ENV PROJECT_ROOT /srv/http
RUN pacman -Syu --noconfirm base-devel lynx nano postgresql git \
uwsgi uwsgi-plugin-python uwsgitop \
python python-{pip,setuptools,wheel} && \
pip install --upgrade pip setuptools wheel uwsgi && \
pacman -Scc --noconfirm
RUN useradd --create-home $user
ENV SLEEKFORUM_USER=$user
USER $SLEEKFORUM_USER
ENV SLEEKFORUM_PATH $PROJECT_ROOT/$SLEEKFORUM_USER
ARG dev_env=local
COPY --chown=$SLEEKFORUM_USER . $SLEEKFORUM_PATH
WORKDIR $SLEEKFORUM_PATH
ENV SETTINGS_ENV flyforum_project.settings.$dev_env
ENV REQUIREMENT_ENV flyforum_project/requirements/$dev_env.txt
RUN pip install -r $REQUIREMENTS_ENV --no-warn-script-location
EXPOSE 4042
CMD ["uwsgi", "uwsgi.ini"]