# schema_generator.py
import sqlite3
from typing import get_type_hints
from models.base import Model

class SchemaGenerator:
    def __init__(self, models: list[type[Model]], conn: sqlite3.Connection):
        self.models = models
        self.conn = conn
        self.cursor = self.conn.cursor()

    def map_type(self, typ):
        if typ == int:
            return "INTEGER"
        elif typ == str:
            return "TEXT"
        elif typ == float:
            return "REAL"
        elif isinstance(typ, type) and issubclass(typ, Model):
            return "INTEGER"
        else:
            raise Exception(f"Unsupported type: {typ}")

    def generate(self):
        for model in self.models:
            if not issubclass(model, Model):
                raise TypeError(f"Class '{model.__name__}' must inherit from Model to be used as an ORM entity.")

            table_name = model.__name__.lower()
            columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
            foreign_keys = []

            hints = get_type_hints(model)
            for field, typ in hints.items():
                if isinstance(typ, type) and issubclass(typ, Model):
                    fk_field = f"{field}_id"
                    ref_table = typ.__name__.lower()
                    columns.append(f"{fk_field} {self.map_type(typ)}")
                    foreign_keys.append(f"FOREIGN KEY ({fk_field}) REFERENCES {ref_table}(id)")
                else:
                    columns.append(f"{field} {self.map_type(typ)}")

            all_columns = columns + foreign_keys
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(all_columns)});"
            print(f"[SQL] {sql}")
            self.cursor.execute(sql)
        self.conn.commit()

