FROM debian:stretch

RUN apt-get update && apt-get install -y python3 python3-pip knot-dnsutils bind9 vim procps && apt-get autoclean
RUN pip3 install connexion[swagger-ui] dnspython watchdog[watchmedo]

ADD . /app
# Add zone config to bind9
RUN cat /app/template/zone >> /etc/bind/named.conf.local && \
    # Add configuration for logging
    cp /app/template/named.conf.log /etc/bind/named.conf.log && \
    echo "include \"/etc/bind/named.conf.log\";" >> /etc/bind/named.conf.local && \
    # Add key for allowing updates
    echo "include \"/etc/bind/named.conf.keys\";" >> /etc/bind/named.conf.local && \
    cp /app/template/named.conf.keys /etc/bind/named.conf.keys && \
    # Add example zone
    cp /app/template/db.example.org /etc/bind/db.example.org

# Create log folders and set the right permission for log and /etc/bind
RUN mkdir /var/log/named && \
    touch /var/log/named/general.log && \
    touch /var/log/named/queries.log && \
    touch /var/log/named/default.log && \
    chmod -R 777 /var/log/named && \
    chown -R root:bind /etc/bind && \
    chmod -R 775 /etc/bind

EXPOSE 9090

WORKDIR /app
RUN chmod 755 entrypoint.sh
CMD "/app/entrypoint.sh"
