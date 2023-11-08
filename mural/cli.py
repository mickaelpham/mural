from datetime import datetime
import tomllib
import click
from tabulate import tabulate

from mural.client import Client


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.pass_context
def cli(ctx):
    """Bulk changes CLI tool for Mural."""

    # ensure that ctx.obj exists and is a dict
    ctx.ensure_object(dict)

    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    ctx.obj["client"] = Client(
        config["mural"]["host"],
        config["app"]["client_id"],
        config["app"]["client_secret"],
        config["mural"]["refresh_token"],
    )


@cli.command()
@click.pass_context
def me(ctx):
    """Retrieve informations about myself."""

    me = ctx.obj["client"].get("/api/public/v1/users/me")["value"]
    fields = [
        "id",
        "email",
        "firstName",
        "lastName",
        "type",
        "lastActiveWorkspace",
        "createdOn",
    ]

    # change the created on from a timestamp to a datetime
    me["createdOn"] = datetime.fromtimestamp(me["createdOn"] / 1e3)

    table = list(map(lambda field: [field, me[field]], fields))
    click.echo(tabulate(table))


@cli.command()
@click.pass_context
def workspaces(ctx):
    """Returns all workspaces the authenticated user is a member of, whether the
    workspace or user is active or inactive."""

    workspaces = ctx.obj["client"].get("/api/public/v1/workspaces")["value"]

    for workspace in workspaces:
        click.echo(f"{workspace['id']} | {workspace['name']}")


@cli.command()
@click.argument("workspace_id")
@click.option(
    "--include-members",
    is_flag=True,
    default=False,
    help="Also fetch every room members for each room.",
)
@click.pass_context
def rooms(ctx, workspace_id, include_members):
    """Returns all rooms in a workspace that the authenticated user has read access to.
    The user must have access to both the workspace and the rooms."""

    client = ctx.obj["client"]
    rooms = client.get(f"/api/public/v1/workspaces/{workspace_id}/rooms")["value"]

    if include_members:
        for room in rooms:
            click.echo(f"Members in room \"{room['name']}\" (room id: {room['id']})")

            members = client.get(f"/api/public/v1/rooms/{room['id']}/users")["value"]
            fields = ["id", "firstName", "lastName", "email"]
            table = list(
                map(
                    lambda member: list(map(lambda field: member[field], fields)),
                    members,
                )
            )
            click.echo(tabulate(table, headers=fields))
            click.echo()
    else:
        fields = ["id", "name", "type", "confidential"]
        table = list(
            map(lambda room: list(map(lambda field: room[field], fields)), rooms)
        )
        click.echo(tabulate(table, headers=fields))
        click.echo()
