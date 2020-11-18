clean:
	rm -f ./envoy.yaml ./token.txt

install: envoy.yaml
	-docker pull envoyproxy/envoy:v1.16-latest
	-docker pull python:3.8-slim
	docker-compose build

token.txt:
	docker-compose run \
	  -e CLIENT_ID=${CLIENT_ID} \
	  -e CLIENT_SECRET=${CLIENT_SECRET} \
	  -e API_AUDIENCE=${API_AUDIENCE} \
	  -e AUTH0_DOMAIN=${AUTH0_DOMAIN} \
	  app python /get_token.py > ./token.txt

envoy.yaml:
	cat ./envoy.tmpl.yaml | envsubst > ./envoy.yaml

run: install
	docker-compose down
	docker-compose up -d
