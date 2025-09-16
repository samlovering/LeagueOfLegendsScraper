
FROM mariadb:11.3

ENV MYSQL_DATABASE=league_db
ENV MYSQL_USER=league_user
ENV MYSQL_PASSWORD=league_pass

EXPOSE 3306

CMD export MARIADB_LINK="mariadb://$MYSQL_USER:$MYSQL_PASSWORD@localhost:3306/$MYSQL_DATABASE" && \
    echo "MariaDB connection link: $MARIADB_LINK"