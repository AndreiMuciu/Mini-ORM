from models.author import Author
from models.base import Model

class Book(Model):
    title: str
    author: Author
    genre: str