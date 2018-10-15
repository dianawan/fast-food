import os
import click
from flask import Flask
from app import create_app
from app.database import CreateTables

app = create_app(os.getenv("APP_SETTINGS") or "default")

if __name__ == '__main__':
    app.run()
