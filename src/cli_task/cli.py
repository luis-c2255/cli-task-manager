import sys, click
from .db import init_db
from .tasks import create_task, list_tasks, update_task, delete_task, get_tasks


@click.group()
def cli():
	"""CLI Task Manager"""

@cli.command()
def init():
	"""Initialize the tasks database."""
	init_db()
	click.echo("Initialized database at ~/.config/cli-task/tasks.db")

@cli.command()
@click.argument("title")
@click.option("--description", "-d", default="", help="Task description")
@click.option("--due", "-u", default="", help="Due date (DD-MM-YYYY)")
@click.option("--priority", "-p", type=int, default=1, help="Priority level")
def add(title, description, due, priority):
	"""Add a new task."""
	try:
		task_id = create_task(title, description, due, priority)
		click.echo(f"Task {task_id} created: {title}")
	except ValueError as e:
		click.echo(f"Error: {e}")

@cli.command()
@click.argument("task_id", type=int)
@click.option("--title", help="New title")
@click.option("--description", help="New description")
@click.option("--due", help="New due date (DD-MM-YYYY)")
@click.option("--priority", type=int, help="New priority level")
@click.option("--status", type=click.Choice(["pending", "done"]), help="New status")

def update(task_id, title, description, due, priority, status):
	"""Update an existing task by ID."""
	fields = {k: v for k, v in {
		"title": title, "description": description,
		"due_date": due, "priority": priority, "status": status
	}.items() if v is not None}
	try:
		update_task(task_id, **fields)
		click.echo(f"Task {task_id} updated.")
	except ValueError as e:
		click.echo(f"Error: {e}")

@cli.command()
@click.argument("task_id", type=int)
def delete(task_id):
	"""Delete a task by ID."""
	try:
		delete_task(task_id)
		click.echo(f"Task {task_id} deleted.")
	except ValueError as e:
		click.echo(f"Error: {e}")

@cli.command(name="list")
def _list():
	"""List all tasks."""
	tasks = list_tasks()
	if not tasks:
		click.echo("No tasks found.")
		return

	click.echo(f"{'ID':<4} {'Title':<50} {'Due':<10} {'P':<3} {'Status'}")
	for id, title, due, prio, status in tasks:
		title_display = (title[:47] + "...") if len(title) > 50 else title
		click.echo(f"{id:<4} {title_display:<50} {due or '':<10} {prio:<3} {status}")	 

if __name__ == "__main__":
	cli()