# ----------- Linux
install_pgcli:
	pip install pgcli

enter_db:
	pgcli -h localhost -p 5432 -u postgres -d kemis_data_db


# Dump example: docker exec -it data_lake_db pg_dump -U postgres Kemis_analytics_db > output_file.sql

# Load example: docker exec -it data_lake_db pg_dump -U postgres Kemis_analytics_db | docker cp - ./output_file.sql
