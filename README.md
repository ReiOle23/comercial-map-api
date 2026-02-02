# comercial-map-api
A comercial map api to get company leads


- docker exec -it comercial_map_api bash
- uvicorn comercial_map_api.asgi:application --workers 4 --host 0.0.0.0 --port 8000