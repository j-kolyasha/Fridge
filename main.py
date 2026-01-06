from fridge.core.service import Service
from fridge.data.repository import Repository
from fridge.ui.cli import CLI
from fridge.config import DATA_PATH, UNITS, CATEGORY, LOCATIONS, FIELDS_FOR_FILTERING

if __name__ == "__main__":
    rep = Repository(DATA_PATH)
    srv = Service(rep)
    cli = CLI(srv, UNITS, CATEGORY, LOCATIONS, FIELDS_FOR_FILTERING)
    cli.menu()