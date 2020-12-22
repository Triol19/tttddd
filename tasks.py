import subprocess

import typer

app = typer.Typer()


@app.command()
def migrate() -> None:
    subprocess.run(['alembic', 'upgrade', 'head'])


@app.command()
def docker() -> None:
    subprocess.run(['docker-compose', 'up', '-d'])


@app.command()
def run(port: int = 8000) -> None:
    docker()
    migrate()

    subprocess.run(['python', 'run.py', f'{port}'])


if __name__ == '__main__':
    app()
