from fastapi import FastAPI, Body

app = FastAPI()

class Books:
    id:int
    title:str
    author:str
    description:str
    rating:int
    
    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        
books = [
    Books(1, "The Time Machine", "H. G. Wells", "A scientist travels through time.", 5),
    Books(2, "The War of the Worlds", "H. G. Wells", "Aliens invade Earth.", 4),
    Books(3, "Dune", "Frank Herbert", "A sci-fi epic on the desert planet Arrakis.", 5),
    Books(4, "Foundation", "Isaac Asimov", "A mathematician predicts the future of civilization.", 5),
    Books(5, "Ender's Game", "Orson Scott Card", "A young genius trains for an alien war.", 5),
    Books(6, "Clean Code", "Robert C. Martin", "A guide to writing clean and maintainable code.", 5),
    Books(7, "Fluent Python", "Luciano Ramalho", "Advanced concepts of Python programming.", 5),
    Books(8, "Python Crash Course", "Eric Matthes", "A beginner-friendly Python guide.", 4),
    Books(9, "Atomic Habits", "James Clear", "Build good habits and break bad ones.", 5),
    Books(10, "Think Like a Monk", "Jay Shetty", "Lessons on living a meaningful life.", 4),
    Books(11, "Deep Work", "Cal Newport", "Master focused work in a distracted world.", 5),
    Books(12, "The Hobbit", "J. R. R. Tolkien", "A hobbit's unexpected adventure.", 5),
    Books(13, "The Fellowship of the Ring", "J. R. R. Tolkien", "The first journey of the Fellowship.", 5),
    Books(14, "Harry Potter and the Philosopher's Stone", "J. K. Rowling", "A boy discovers he is a wizard.", 5),
    Books(15, "A Game of Thrones", "George R. R. Martin", "Noble families fight for the Iron Throne.", 5),
    Books(16, "A Brief History of Time", "Stephen Hawking", "An introduction to cosmology.", 5),
    Books(17, "Cosmos", "Carl Sagan", "A journey through the universe.", 5),
    Books(18, "The Alchemist", "Paulo Coelho", "A shepherd follows his dreams.", 5),
    Books(19, "The Kite Runner", "Khaled Hosseini", "A story of friendship and redemption.", 5),
    Books(20, "Rich Dad Poor Dad", "Robert Kiyosaki", "Lessons on financial literacy.", 4),
    Books(21, "The Psychology of Money", "Morgan Housel", "Understanding human behavior with money.", 5),
    Books(22, "1984", "George Orwell", "A dystopian society under constant surveillance.", 5),
    Books(23, "Brave New World", "Aldous Huxley", "A futuristic world shaped by technology.", 5),
    Books(24, "The Shining", "Stephen King", "A haunted hotel terrorizes a family.", 5),
    Books(25, "Dracula", "Bram Stoker", "The classic vampire novel.", 5),
    Books(26, "The Da Vinci Code", "Dan Brown", "A mystery involving secret societies.", 4),
    Books(27, "Gone Girl", "Gillian Flynn", "A psychological thriller with twists.", 5),
    Books(28, "Pride and Prejudice", "Jane Austen", "A timeless romance and social commentary.", 5),
    Books(29, "To Kill a Mockingbird", "Harper Lee", "Justice and morality in the American South.", 5),
    Books(30, "Moby-Dick", "Herman Melville", "A captain's obsession with a white whale.", 4),
]

@app.get("/books")
async def read_all_books():
    return books



@app.post("/book/create")
async def create_book(book = Body()):
    books.append(book)
    return book
    






