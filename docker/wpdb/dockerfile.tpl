FROM mysql:5.7

RUN sed -i -e 's/^\(mysql:[^:]\):[0-9]*:[0-9]*:/\1:<UID>:<GID>:/' /etc/passwd
