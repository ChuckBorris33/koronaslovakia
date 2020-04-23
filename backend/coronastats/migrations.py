import click
from coronastats import db_wrapper
from coronastats.db import CoronaLog, CoronaLocationLog, CoronaLocation
from flask import current_app
from playhouse.migrate import SqliteMigrator, migrate

app = current_app


def init_database(database):
    def front():
        database.create_tables([CoronaLog])

    def back():
        database.execute_sql("DROP TABLE IF EXISTS coronalog;")

    return front, back


def add_location_tables(database):
    def front():
        database.create_tables([CoronaLocationLog, CoronaLocation])

    def back():
        database.execute_sql("DROP TABLE IF EXISTS coronalocationlog;")
        database.execute_sql("DROP TABLE IF EXISTS coronalocation;")

    return front, back


def rename_corona_log_datetime(database):
    migrator = SqliteMigrator(database)

    def front():
        try:
            migrate(migrator.rename_column("coronalog", "datetime", "date"))
        except ValueError:
            pass

    def back():
        try:
            migrate(migrator.rename_column("coronalog", "date", "datetime"))
        except ValueError:
            pass

    return front, back


migrations = [init_database, add_location_tables, rename_corona_log_datetime]


def get_migration_state():
    database = db_wrapper.database
    return database.execute_sql("PRAGMA user_version;").fetchone()[0]


def set_migration_state(version):
    database = db_wrapper.database
    return database.execute_sql(f"PRAGMA user_version={int(version)};")


def run_migrations(goal_version):
    database = db_wrapper.database
    current_state = get_migration_state()
    with database.atomic() as transaction:
        try:
            if current_state < goal_version:
                migrations_to_apply = migrations[current_state:goal_version]
                for migration in migrations_to_apply:
                    click.echo(f"Applying {migration.__name__}")
                    front, _ = migration(database)
                    front()
                set_migration_state(goal_version)
            elif current_state > goal_version:
                migrations_to_apply = reversed(migrations[goal_version:current_state])
                for migration in migrations_to_apply:
                    click.echo(f"Unapplying {migration.__name__}")
                    _, back = migration(database)
                    back()
                set_migration_state(goal_version)
            else:
                click.echo("No migrations to apply")
        except Exception:
            transaction.rollback()
            click.secho(f"Error migrating. Rolling back.", fg="red")
            raise


def show_migrations():
    current_state = get_migration_state()
    for index, migration in enumerate(migrations, 1):
        color = "green" if current_state >= index else "red"
        bold = current_state >= index
        click.secho(f"{index}\t{migration.__name__}", fg=color, bold=bold)
