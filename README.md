# comercial-map-api
A comercial map api to get company leads by params

To start app:
```bash
# Build the app
docker-compose build

# Run the app
docker-compose up
```

The app will be available at `http://localhost:58900`

To run tests:
```bash
# test 1000 request may fail sometimes due to database connection limits
docker exec -it comercial_map_api pytest
```
