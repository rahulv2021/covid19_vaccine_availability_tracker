docker-build:
	@docker build -t tracker:1.0 .

docker-run: docker-build
	@docker run -d --rm --name v_tracker tracker:1.0
