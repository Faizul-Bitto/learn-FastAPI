from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Books:
    id:int
    title:str
    author:str
    description:str
    rating:int
    published_date:int
    
    def __init__(self, id, title, author, description, rating, published_year):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year

class BookRequest(BaseModel):
    id:Optional[int] = Field(description="id is not needed or need to be created", default=None) #! it can be either integer or can be a type 'None'
    # id: int | None = None #! without using Optional
    title:str = Field(min_length=3) #! minimum length of 3
    author:str = Field(min_length=1) #! minimum length of 1
    description:str = Field(min_length=1, max_length=100) #! minimum length of 1, maximum length of 100
    rating:int = Field(gt=0,lt=6) #! gt (greater than), lt (less than)
    published_year:int = Field(description="Publication year", examples=[2012])
    
    model_config = {
        "json_schema_extra" : {
            "example" : {
                "title": "A new book",
                "author": "A new author",
                "description": "A new description of the new book",
                "rating": 5,
                "published_year" : 2012
            }
        }
    }
        
books = [
    Books(1, "The Time Machine", "H. G. Wells", "A scientist travels through time.", 5, 1895),
    Books(2, "The War of the Worlds", "H. G. Wells", "Aliens invade Earth.", 4, 1898),
    Books(3, "Dune", "Frank Herbert", "A sci-fi epic on the desert planet Arrakis.", 5, 1965),
    Books(4, "Foundation", "Isaac Asimov", "A mathematician predicts the future of civilization.", 5, 1951),
    Books(5, "Ender's Game", "Orson Scott Card", "A young genius trains for an alien war.", 5, 1985),
    Books(6, "Clean Code", "Robert C. Martin", "A guide to writing clean and maintainable code.", 5, 2008),
    Books(7, "Fluent Python", "Luciano Ramalho", "Advanced Python programming concepts.", 5, 2015),
    Books(8, "Python Crash Course", "Eric Matthes", "A beginner-friendly Python guide.", 4, 2015),
    Books(9, "Atomic Habits", "James Clear", "Build good habits and break bad ones.", 5, 2018),
    Books(10, "Think Like a Monk", "Jay Shetty", "Lessons on living a meaningful life.", 4, 2020),
    Books(11, "Deep Work", "Cal Newport", "Master focused work in a distracted world.", 5, 2016),
    Books(12, "The Hobbit", "J. R. R. Tolkien", "A hobbit's unexpected adventure.", 5, 1937),
    Books(13, "The Fellowship of the Ring", "J. R. R. Tolkien", "The first journey of the Fellowship.", 5, 1954),
    Books(14, "The Two Towers", "J. R. R. Tolkien", "The Fellowship is broken.", 5, 1954),
    Books(15, "The Return of the King", "J. R. R. Tolkien", "The final battle for Middle-earth.", 5, 1955),
    Books(16, "Harry Potter and the Philosopher's Stone", "J. K. Rowling", "A boy discovers he is a wizard.", 5, 1997),
    Books(17, "Harry Potter and the Chamber of Secrets", "J. K. Rowling", "The second year at Hogwarts.", 5, 1998),
    Books(18, "Harry Potter and the Prisoner of Azkaban", "J. K. Rowling", "Sirius Black escapes prison.", 5, 1999),
    Books(19, "A Game of Thrones", "George R. R. Martin", "Noble families fight for the Iron Throne.", 5, 1996),
    Books(20, "A Clash of Kings", "George R. R. Martin", "The war for the throne intensifies.", 5, 1998),
    Books(21, "A Storm of Swords", "George R. R. Martin", "Betrayal and war reshape Westeros.", 5, 2000),
    Books(22, "A Brief History of Time", "Stephen Hawking", "An introduction to cosmology.", 5, 1988),
    Books(23, "Cosmos", "Carl Sagan", "A journey through the universe.", 5, 1980),
    Books(24, "The Alchemist", "Paulo Coelho", "A shepherd follows his dreams.", 5, 1988),
    Books(25, "The Kite Runner", "Khaled Hosseini", "A story of friendship and redemption.", 5, 2003),
    Books(26, "Rich Dad Poor Dad", "Robert Kiyosaki", "Lessons on financial literacy.", 4, 1997),
    Books(27, "The Psychology of Money", "Morgan Housel", "Understanding human behavior with money.", 5, 2020),
    Books(28, "1984", "George Orwell", "A dystopian society under constant surveillance.", 5, 1949),
    Books(29, "Animal Farm", "George Orwell", "A political allegory on revolution.", 5, 1945),
    Books(30, "Brave New World", "Aldous Huxley", "A futuristic world shaped by technology.", 5, 1932),
    Books(31, "The Shining", "Stephen King", "A haunted hotel terrorizes a family.", 5, 1977),
    Books(32, "It", "Stephen King", "An ancient evil terrorizes children.", 5, 1986),
    Books(33, "Dracula", "Bram Stoker", "The classic vampire novel.", 5, 1897),
    Books(34, "Frankenstein", "Mary Shelley", "A scientist creates life.", 5, 1818),
    Books(35, "The Da Vinci Code", "Dan Brown", "A mystery involving secret societies.", 4, 2003),
    Books(36, "Angels & Demons", "Dan Brown", "A race against time in Vatican City.", 4, 2000),
    Books(37, "Gone Girl", "Gillian Flynn", "A psychological thriller with twists.", 5, 2012),
    Books(38, "The Girl with the Dragon Tattoo", "Stieg Larsson", "A journalist investigates a mystery.", 5, 2005),
    Books(39, "Pride and Prejudice", "Jane Austen", "A timeless romance and social commentary.", 5, 1813),
    Books(40, "Sense and Sensibility", "Jane Austen", "Love and family in Regency England.", 5, 1811),
    Books(41, "To Kill a Mockingbird", "Harper Lee", "Justice and morality in the American South.", 5, 1960),
    Books(42, "Moby-Dick", "Herman Melville", "A captain's obsession with a white whale.", 4, 1851),
    Books(43, "The Catcher in the Rye", "J. D. Salinger", "A teenager struggles with identity.", 4, 1951),
    Books(44, "The Great Gatsby", "F. Scott Fitzgerald", "The American dream and tragedy.", 5, 1925),
    Books(45, "The Lord of the Flies", "William Golding", "Boys stranded on an island.", 5, 1954),
    Books(46, "The Chronicles of Narnia", "C. S. Lewis", "Children discover a magical world.", 5, 1950),
    Books(47, "The Martian", "Andy Weir", "An astronaut survives alone on Mars.", 5, 2011),
    Books(48, "Project Hail Mary", "Andy Weir", "A lone astronaut saves humanity.", 5, 2021),
    Books(49, "The Silent Patient", "Alex Michaelides", "A woman stops speaking after a murder.", 5, 2019),
    Books(50, "Sapiens", "Yuval Noah Harari", "A brief history of humankind.", 5, 2011),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return books

@app.get("/book/{id}", status_code=status.HTTP_200_OK)
async def fetch_book_by_id(id:int = Path(gt=0)):
    for book in books:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/book/", status_code=status.HTTP_200_OK)
async def fetch_book_by_rating(rating:int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in books:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/book/filter_by_published_year/", status_code=status.HTTP_200_OK)
async def fetch_book_by_publish_year(published_year:int):
    books_to_return = []
    for book in books:
        if book.published_year == published_year:
            books_to_return.append(book)           
    return books_to_return

# @app.post("/book/create")
# async def create_book(book = Body()):
#     books.append(book)
#     return book
    
@app.post("/book/create", status_code=status.HTTP_201_CREATED)
async def create_book(create_book_request: BookRequest):
    print(type(create_book_request))
    new_book = Books(**create_book_request.model_dump())
    books.append(find_book_id(new_book))
    print(type(new_book))
    return new_book

def find_book_id(book:Books):
    book.id = 1 if len(books) == 0 else books[-1].id + 1
    # if len(books) > 0:
    #     book.id = books[-1].id + 1
    # else:
    #     book.id = 1
    return book

@app.put("/book/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    for i in range(len(books)):
        if books[i].id == book.id:
            books[i] = Books(**book.model_dump())
            return books[i]
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/book/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int = Path(gt=0)):
    for i in range(len(books)):
        if books[i].id == id:
            return books.pop(i)
    raise HTTPException(status_code=404, detail="Item not found")
