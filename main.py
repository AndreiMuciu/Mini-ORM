from models.person import Person
from models.author import Author
from models.book import Book
from orm.schemaGenerator import SchemaGenerator
from orm.entityManager import EntityManager
import sqlite3

class Hacker:
    name: str
    mastery: str

conn = sqlite3.connect("literatura.db")

gen = SchemaGenerator([Person, Author, Book], conn)
gen.generate()

em = EntityManager(conn)

h = Hacker()
h.name = "Ion Luca Caragiale"
h.mastery = "Dramaturgie"
#em.save(h)

p = Person()
p.name = "Ion Creangă"
p.age = 45
em.save(p)

a = Author()
a.name = "George Coșbuc"
a.age = 50
a.writingStyle = "Romantic"
em.save(a)

b = Book()
b.title = "Poezii"
b.author = p
b.genre = "Poezie"
#em.save(b)

b1 = Book()
b1.title = "Scrisori către soția mea"
b1.author = a
b1.genre = "Epistolă"
em.save(b1)

b2 = Book()
b2.title = "Luceafărul"
b2.author = a   
b2.genre = "Poezie"
em.save(b2)