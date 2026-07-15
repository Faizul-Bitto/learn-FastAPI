from fastapi import Body, FastAPI

app = FastAPI()

books = [
    {"id": 1, "title": "The Time Machine", "author": "H. G. Wells", "category": "Science Fiction"},
    {"id": 2, "title": "The War of the Worlds", "author": "H. G. Wells", "category": "Science Fiction"},
    {"id": 3, "title": "The Invisible Man", "author": "H. G. Wells", "category": "Science Fiction"},
    {"id": 4, "title": "Dune", "author": "Frank Herbert", "category": "Science Fiction"},
    {"id": 5, "title": "Foundation", "author": "Isaac Asimov", "category": "Science Fiction"},
    {"id": 6, "title": "Ender's Game", "author": "Orson Scott Card", "category": "Science Fiction"},

    {"id": 7, "title": "Python Basics", "author": "John Smith", "category": "Programming"},
    {"id": 8, "title": "Python Advanced", "author": "John Smith", "category": "Programming"},
    {"id": 9, "title": "Mastering Python", "author": "John Smith", "category": "Programming"},
    {"id": 10, "title": "Clean Code", "author": "Robert C. Martin", "category": "Programming"},
    {"id": 11, "title": "Clean Architecture", "author": "Robert C. Martin", "category": "Programming"},
    {"id": 12, "title": "The Clean Coder", "author": "Robert C. Martin", "category": "Programming"},
    {"id": 13, "title": "Fluent Python", "author": "Luciano Ramalho", "category": "Programming"},
    {"id": 14, "title": "Automate the Boring Stuff with Python", "author": "Al Sweigart", "category": "Programming"},
    {"id": 15, "title": "Python Crash Course", "author": "Eric Matthes", "category": "Programming"},

    {"id": 16, "title": "Atomic Habits", "author": "James Clear", "category": "Self Help"},
    {"id": 17, "title": "Think Like a Monk", "author": "Jay Shetty", "category": "Self Help"},
    {"id": 18, "title": "The 7 Habits of Highly Effective People", "author": "Stephen R. Covey", "category": "Self Help"},
    {"id": 19, "title": "Deep Work", "author": "Cal Newport", "category": "Self Help"},
    {"id": 20, "title": "The Power of Habit", "author": "Charles Duhigg", "category": "Self Help"},

    {"id": 21, "title": "The Hobbit", "author": "J. R. R. Tolkien", "category": "Fantasy"},
    {"id": 22, "title": "The Fellowship of the Ring", "author": "J. R. R. Tolkien", "category": "Fantasy"},
    {"id": 23, "title": "The Two Towers", "author": "J. R. R. Tolkien", "category": "Fantasy"},
    {"id": 24, "title": "The Return of the King", "author": "J. R. R. Tolkien", "category": "Fantasy"},
    {"id": 25, "title": "Harry Potter and the Philosopher's Stone", "author": "J. K. Rowling", "category": "Fantasy"},
    {"id": 26, "title": "Harry Potter and the Chamber of Secrets", "author": "J. K. Rowling", "category": "Fantasy"},
    {"id": 27, "title": "Harry Potter and the Prisoner of Azkaban", "author": "J. K. Rowling", "category": "Fantasy"},
    {"id": 28, "title": "Harry Potter and the Goblet of Fire", "author": "J. K. Rowling", "category": "Fantasy"},
    {"id": 29, "title": "A Game of Thrones", "author": "George R. R. Martin", "category": "Fantasy"},
    {"id": 30, "title": "The Name of the Wind", "author": "Patrick Rothfuss", "category": "Fantasy"},
    {"id": 31, "title": "The Way of Kings", "author": "Brandon Sanderson", "category": "Fantasy"},

    {"id": 32, "title": "A Brief History of Time", "author": "Stephen Hawking", "category": "Science"},
    {"id": 33, "title": "The Universe in a Nutshell", "author": "Stephen Hawking", "category": "Science"},
    {"id": 34, "title": "Black Holes and Baby Universes", "author": "Stephen Hawking", "category": "Science"},
    {"id": 35, "title": "Cosmos", "author": "Carl Sagan", "category": "Science"},
    {"id": 36, "title": "The Selfish Gene", "author": "Richard Dawkins", "category": "Science"},
    {"id": 37, "title": "The Gene", "author": "Siddhartha Mukherjee", "category": "Science"},

    {"id": 38, "title": "The Alchemist", "author": "Paulo Coelho", "category": "Fiction"},
    {"id": 39, "title": "Brida", "author": "Paulo Coelho", "category": "Fiction"},
    {"id": 40, "title": "Veronika Decides to Die", "author": "Paulo Coelho", "category": "Fiction"},
    {"id": 41, "title": "The Kite Runner", "author": "Khaled Hosseini", "category": "Fiction"},
    {"id": 42, "title": "Life of Pi", "author": "Yann Martel", "category": "Fiction"},
    {"id": 43, "title": "The Book Thief", "author": "Markus Zusak", "category": "Fiction"},

    {"id": 44, "title": "Rich Dad Poor Dad", "author": "Robert Kiyosaki", "category": "Finance"},
    {"id": 45, "title": "Cashflow Quadrant", "author": "Robert Kiyosaki", "category": "Finance"},
    {"id": 46, "title": "The Business of the 21st Century", "author": "Robert Kiyosaki", "category": "Finance"},
    {"id": 47, "title": "The Intelligent Investor", "author": "Benjamin Graham", "category": "Finance"},
    {"id": 48, "title": "The Psychology of Money", "author": "Morgan Housel", "category": "Finance"},
    {"id": 49, "title": "Your Money or Your Life", "author": "Vicki Robin", "category": "Finance"},

    {"id": 50, "title": "1984", "author": "George Orwell", "category": "Dystopian"},
    {"id": 51, "title": "Animal Farm", "author": "George Orwell", "category": "Dystopian"},
    {"id": 52, "title": "Brave New World", "author": "Aldous Huxley", "category": "Dystopian"},
    {"id": 53, "title": "Fahrenheit 451", "author": "Ray Bradbury", "category": "Dystopian"},
    {"id": 54, "title": "The Handmaid's Tale", "author": "Margaret Atwood", "category": "Dystopian"},

    {"id": 55, "title": "The Shining", "author": "Stephen King", "category": "Horror"},
    {"id": 56, "title": "It", "author": "Stephen King", "category": "Horror"},
    {"id": 57, "title": "Misery", "author": "Stephen King", "category": "Horror"},
    {"id": 58, "title": "Dracula", "author": "Bram Stoker", "category": "Horror"},
    {"id": 59, "title": "Frankenstein", "author": "Mary Shelley", "category": "Horror"},
    {"id": 60, "title": "The Haunting of Hill House", "author": "Shirley Jackson", "category": "Horror"},

    {"id": 61, "title": "The Da Vinci Code", "author": "Dan Brown", "category": "Thriller"},
    {"id": 62, "title": "Angels & Demons", "author": "Dan Brown", "category": "Thriller"},
    {"id": 63, "title": "Inferno", "author": "Dan Brown", "category": "Thriller"},
    {"id": 64, "title": "The Silent Patient", "author": "Alex Michaelides", "category": "Thriller"},
    {"id": 65, "title": "Gone Girl", "author": "Gillian Flynn", "category": "Thriller"},
    {"id": 66, "title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "category": "Thriller"},

    {"id": 67, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Classic"},
    {"id": 68, "title": "This Side of Paradise", "author": "F. Scott Fitzgerald", "category": "Classic"},
    {"id": 69, "title": "Pride and Prejudice", "author": "Jane Austen", "category": "Classic"},
    {"id": 70, "title": "Sense and Sensibility", "author": "Jane Austen", "category": "Classic"},
    {"id": 71, "title": "Emma", "author": "Jane Austen", "category": "Classic"},
    {"id": 72, "title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "Classic"},
    {"id": 73, "title": "Moby-Dick", "author": "Herman Melville", "category": "Classic"},
    {"id": 74, "title": "Jane Eyre", "author": "Charlotte Brontë", "category": "Classic"},
    {"id": 75, "title": "On Writing", "author": "Stephen King", "category": "Self Help"},
    {"id": 76, "title": "Different Seasons", "author": "Stephen King", "category": "Fiction"},

    {"id": 77, "title": "The Casual Vacancy", "author": "J. K. Rowling", "category": "Fiction"},
    {"id": 78, "title": "The Cuckoo's Calling", "author": "Robert Galbraith", "category": "Thriller"},

    {"id": 79, "title": "The Casual Vacancy", "author": "Robert Galbraith", "category": "Fiction"},

    {"id": 80, "title": "Outliers", "author": "Malcolm Gladwell", "category": "Self Help"},
    {"id": 81, "title": "Talking to Strangers", "author": "Malcolm Gladwell", "category": "Psychology"},

    {"id": 82, "title": "Sapiens", "author": "Yuval Noah Harari", "category": "History"},
    {"id": 83, "title": "Homo Deus", "author": "Yuval Noah Harari", "category": "Science"},

    {"id": 84, "title": "The Power of Now", "author": "Eckhart Tolle", "category": "Self Help"},
    {"id": 85, "title": "A New Earth", "author": "Eckhart Tolle", "category": "Spirituality"},

    {"id": 86, "title": "Digital Fortress", "author": "Dan Brown", "category": "Science Fiction"},
    {"id": 87, "title": "Deception Point", "author": "Dan Brown", "category": "Science Fiction"},

    {"id": 88, "title": "Norwegian Wood", "author": "Haruki Murakami", "category": "Fiction"},
    {"id": 89, "title": "Kafka on the Shore", "author": "Haruki Murakami", "category": "Fantasy"},
    {"id": 90, "title": "1Q84", "author": "Haruki Murakami", "category": "Science Fiction"},

    {"id": 91, "title": "The Martian", "author": "Andy Weir", "category": "Science Fiction"},
    {"id": 92, "title": "Project Hail Mary", "author": "Andy Weir", "category": "Science Fiction"},

    {"id": 93, "title": "The Lean Startup", "author": "Eric Ries", "category": "Business"},
    {"id": 94, "title": "Startup Way", "author": "Eric Ries", "category": "Business"},

    {"id": 95, "title": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "category": "Psychology"},
    {"id": 96, "title": "Noise", "author": "Daniel Kahneman", "category": "Business"},

    {"id": 97, "title": "Educated", "author": "Tara Westover", "category": "Memoir"},
    {"id": 98, "title": "Becoming", "author": "Michelle Obama", "category": "Memoir"},
    {"id": 99, "title": "Steve Jobs", "author": "Walter Isaacson", "category": "Biography"},
    {"id": 100, "title": "Einstein", "author": "Walter Isaacson", "category": "Biography"}
]

# GET Method
@app.get("/books")
async def read_all_books():
    return books

@app.get("/books/{book_title}") #! path parameter
async def read_all_books(book_title : str):
    for book in books:
        if book.get("title").casefold() == book_title.casefold():
            return book
        
@app.get("/books/") #! query parameter
async def read_category_by_query(category : str):
    books_to_return = []
    for book in books:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_author}/") #! path + query both
async def read_category_by_query(book_author : str, category : str):
    books_to_return = []
    for book in books:
        if book.get("category").casefold() == category.casefold() and book.get("author").casefold() == book_author.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/fetch_by_specific_author/{book_author}")
async def read_books_by_author(book_author : str):
    books_to_return = []
    for book in books:
        if book.get("author").casefold() == book_author.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/fetch_by_specific_author/query_params/")
async def read_books_by_author(book_author : str):
    books_to_return = []
    for book in books:
        if book.get("author").casefold() == book_author.casefold():
            books_to_return.append(book)
    return books_to_return

# POST Method
@app.post("/books/create_book")
async def create_book(new_book = Body()):
    books.append(new_book)
    return new_book

# PUT Method
@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(books)):
        if books[i].get("id") == updated_book.get("id"):
            books[i] = updated_book
    return updated_book

# DELETE Method
@app.delete("/books/delete_book/{book_id}")
async def delete_book(book_id : int):
    for i in range(len(books)):
        if books[i].get("id") == book_id:
            books.pop(i)
            return {"message": "Book deleted"}