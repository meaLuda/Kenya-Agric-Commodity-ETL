etl_flow:
	docker compose exec prefect_flow prefect deployment create /opt/prefect/flows/data_pipeline.py:etl_flow

run_flow:
	docker compose exec prefect_flow prefect deployment run etl_flow/etl_flow