from typing import get_type_hints
from models.base import Model

class EntityManager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def save(self, obj: Model):
        table_name = obj.__class__.__name__.lower()
        fields = []
        values = []
        hints = get_type_hints(obj.__class__)

        for field_name, field_type in hints.items():
            value = getattr(obj, field_name)

            if isinstance(value, Model):
                if not isinstance(value, field_type):
                    raise Exception(
                        f"Invalid object type for field '{field_name}'. "
                        f"Expected {field_type.__name__}, got {type(value).__name__}."
                    )

                fk_value = getattr(value, "id", None)
                if fk_value is None:
                    raise Exception(f"Referenced object for field '{field_name}' must be saved before.")
                fields.append(f"{field_name}_id")
                values.append(fk_value)
            else:
                fields.append(field_name)
                values.append(value)

        placeholders = ", ".join(["?"] * len(values))
        sql = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders});"

        print("[SAVE]", sql, values)
        self.cursor.execute(sql, values)

        obj.id = self.cursor.lastrowid  
        self.conn.commit()
