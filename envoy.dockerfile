FROM envoyproxy/envoy:v1.16-latest
CMD ["envoy", "-c", "/etc/envoy.yaml"]
COPY ./envoy.yaml /etc/envoy.yaml
