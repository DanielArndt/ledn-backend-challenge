# ledn-backend-challenge

## Requirements

- `docker`
- `docker compose`

## Build and run the platform

```
docker compose up --build
```

## Run integration tests

While the docker-compose instance is up and running
```bash
docker exec -it ledn-backend-challenge-python_api-1 sh -c "pytest test/test_api.py"
```
