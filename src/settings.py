import os
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_user = os.getenv('POSTGRES_USER')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_database = os.getenv('POSTGRES_DATABASE')
postgres_schema = os.getenv('POSTGRES_SCHEMA')
alembic_revision = os.getenv('ALEMBIC_REVISION')
