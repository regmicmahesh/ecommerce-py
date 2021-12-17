
EXEC := poetry run

migrate:
		@$(EXEC) python -m escp.migrations

run:
	@$(EXEC) gunicorn escp:app


