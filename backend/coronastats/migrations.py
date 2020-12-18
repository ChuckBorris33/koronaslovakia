import click
from flask import current_app
from playhouse.migrate import SqliteMigrator, migrate
from peewee import IntegerField

from coronastats import db_wrapper

app = current_app


def init_database(database):
    def front():
        database.execute_sql(
            """
            create table coronalog
            (
                id       INTEGER not null
                    primary key,
                datetime     DATE    not null,
                infected INTEGER not null,
                cured    INTEGER not null,
                tests    INTEGER not null,
                deaths   INTEGER not null
            );
            create unique index coronalog_date
                on coronalog (date);
        """
        )

    def back():
        database.execute_sql("DROP TABLE IF EXISTS coronalog;")

    return front, back


def add_location_tables(database):
    def front():
        database.execute_sql(
            """
            create table coronalocation
            (
                id           INTEGER      not null
                    primary key,
                location     VARCHAR(255) not null,
                last_updated DATE         not null
            );
            create index coronalocation_location
                on coronalocation (location);
            create table coronalocationlog
            (
                id               INTEGER not null
                    primary key,
                date             DATE    not null,
                infected         INTEGER not null,
                infected_females INTEGER not null,
                cured            INTEGER not null,
                tests            INTEGER not null,
                deaths           INTEGER not null,
                location_id      INTEGER not null
                    references coronalocation
            );
            create index coronalocationlog_date
                on coronalocationlog (date);
            create index coronalocationlog_location_id
                on coronalocationlog (location_id);
        """
        )

    def back():
        database.execute_sql("DROP TABLE IF EXISTS coronalocationlog;")
        database.execute_sql("DROP TABLE IF EXISTS coronalocation;")

    return front, back


def rename_corona_log_datetime(database):
    migrator = SqliteMigrator(database)

    def front():
        migrate(migrator.rename_column("coronalog", "datetime", "date"))

    def back():
        migrate(migrator.rename_column("coronalog", "date", "datetime"))

    return front, back


def add_additional_corona_log_fields(database):
    migrator = SqliteMigrator(database)

    def front():
        median = IntegerField(default=0)
        hospitalized = IntegerField(default=0)
        confirmed_hospitalized = IntegerField(default=0)
        confirmed_hospitalized_icu = IntegerField(default=0)
        confirmed_hospitalized_ventilation = IntegerField(default=0)

        migrate(
            migrator.add_column("coronalog", "median", median),
            migrator.add_column("coronalog", "hospitalized", hospitalized),
            migrator.add_column(
                "coronalog", "confirmed_hospitalized", confirmed_hospitalized
            ),
            migrator.add_column(
                "coronalog", "confirmed_hospitalized_icu", confirmed_hospitalized_icu
            ),
            migrator.add_column(
                "coronalog",
                "confirmed_hospitalized_ventilation",
                confirmed_hospitalized_ventilation,
            ),
        )

    def back():
        migrate(
            migrator.drop_column("coronalog", "median"),
            migrator.drop_column("coronalog", "hospitalized"),
            migrator.drop_column("coronalog", "confirmed_hospitalized"),
            migrator.drop_column("coronalog", "confirmed_hospitalized_icu"),
            migrator.drop_column("coronalog", "confirmed_hospitalized_ventilation"),
        )

    return front, back


migrations = [
    init_database,
    add_location_tables,
    rename_corona_log_datetime,
    add_additional_corona_log_fields,
]


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
            click.secho("Error migrating. Rolling back.", fg="red")
            raise


def show_migrations():
    current_state = get_migration_state()
    for index, migration in enumerate(migrations, 1):
        color = "green" if current_state >= index else "red"
        bold = current_state >= index
        click.secho(f"{index}\t{migration.__name__}", fg=color, bold=bold)
