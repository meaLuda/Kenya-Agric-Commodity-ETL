# ----------- Linux
install_pgcli:
	pip install pgcli

enter_db:
	pgcli -h localhost -p 5432 -u postgres -d kemis_data_db
