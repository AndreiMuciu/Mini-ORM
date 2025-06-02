# Simplified Object-Relational Mapper (ORM)

## Description

This project is a simplified Object-Relational Mapper (ORM) implemented in Python for the **Software Systems Design and Architecture** course. It includes a schema generator and an entity manager that together allow defining Python classes as database entities, generating corresponding database tables, and persisting objects to an SQLite database.

## Features

- ✅ **Schema Generator**: Automatically creates database tables from annotated Python classes, handling inheritance and associations.
- ✅ **Entity Manager**: Saves object instances into the generated tables, including support for foreign keys (1 bonus point).
- ✅ **Multiple Test Models**: Includes at least two different applications/models to demonstrate ORM functionality (1 bonus point).

## How It Works

### Schema Generator (`orm/schemaGenerator.py`)
- Accepts a list of classes inheriting from `Model`.
- Uses type hints to determine field types.
- Maps Python types (`int`, `str`, `float`) to SQL types.
- Detects associations and generates foreign key constraints.

### Entity Manager (`orm/entityManager.py`)
- Saves objects to the database.
- Resolves relationships by saving foreign key IDs.
- Automatically updates the object's `id` after insertion.

## Example Models

```python
# models/person.py
class Person(Model):
    name: str
    age: int

# models/author.py
class Author(Person):
    writingStyle: str

# models/book.py
class Book(Model):
    title: str
    author: Author
    genre: str
```
## Example Usage
```python
conn = sqlite3.connect("literatura.db")

# Generate schema
gen = SchemaGenerator([Person, Author, Book], conn)
gen.generate()

# Save entities
em = EntityManager(conn)

a = Author()
a.name = "George Coșbuc"
a.age = 50
a.writingStyle = "Romantic"
em.save(a)

b = Book()
b.title = "Luceafărul"
b.author = a
b.genre = "Poezie"
em.save(b)
```
## Project Structure
```bash
.
├── main.py
├── models/
│   ├── author.py
│   ├── base.py
│   ├── book.py
│   └── person.py
└── orm/
    ├── entityManager.py
    └── schemaGenerator.py
