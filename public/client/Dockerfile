FROM alpine:3.4

# Add commonly used packages
RUN apk add --no-cache bind-tools

# Add s6-overlay
ENV S6_OVERLAY_VERSION=v1.17.2.0 \
    GODNSMASQ_VERSION=1.0.6

RUN apk add --no-cache curl && \
    curl -sSL https://github.com/just-containers/s6-overlay/releases/download/${S6_OVERLAY_VERSION}/s6-overlay-amd64.tar.gz \
    | tar xfz - -C / && \
    curl -sSL https://github.com/janeczku/go-dnsmasq/releases/download/${GODNSMASQ_VERSION}/go-dnsmasq-min_linux-amd64 -o /bin/go-dnsmasq && \
    chmod +x /bin/go-dnsmasq && \
    apk del curl &&

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.3/main" >> /etc/apk/repositories && \
    apk add --update nginx=1.10.1-r7 && \
    rm -rf /var/cache/apk/* && \
    chown -R nginx:www-data /var/lib/nginx

ADD root /

ENTRYPOINT ["/init"]

# Expose the ports for nginx
EXPOSE 80 443
