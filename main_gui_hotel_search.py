import os
import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from sqlalchemy import create_engine, func
from sqlalchemy.schema import CreateTable

from data_access.data_generator import *
from gui.hotel_search import *

def init_db() -> Engine:
    data_path = Path(os.getcwd()).joinpath("data")
    data_path.mkdir(exist_ok=True)

    connection_str = f"sqlite:///{data_path}/example.db"
    e = create_engine(connection_str)
    with open(data_path.joinpath("example.ddl"), "w") as ddl_file:
        for table in Base.metadata.tables.values():
            create_table = str(CreateTable(table).compile(e)).strip()
            ddl_file.write(f"{create_table};{os.linesep}")

    Base.metadata.drop_all(e)
    Base.metadata.create_all(e)
    return e

def generate_example_data(e: Engine):
    generate_system_data(e)
    generate_hotels(e)
    generate_guests(e)
    generate_registered_guests(e)


def main():
    engine = init_db()
    generate_example_data(engine)

    # Handle high resolution displays:
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    with Session(engine) as session:
        app = QApplication(sys.argv)
        main_window = HotelTableView(session)
        main_window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
