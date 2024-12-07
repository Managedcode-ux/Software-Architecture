# 1.Data Layer(Persistence Layer)
# simulate database operation

class BookRepository:
    def __init__(self) -> None:
        self.db = {}

    def add_book(self,book):
        self.db[book.id] = book

    def get_book(self,book_id):
        return self.db.get(book_id)

    def get_all_book(self):
        return list(self.db.values())


# --------------
# 2.Business Layer(Domain Layer)
# Contains business entities and core business logic

class Book:
    def __init__(self,id,title,author,is_available=True) -> None:
        self.id = id
        self.title = title
        self.is_available = is_available
        self.author = author

    def __str__(self) -> str:
        return f"Book: {self.title} by {self.author}"


# --------------
# 3. Application Layer (Service Layer)
# Handles business workflows and coordinates operations
class LibraryServices:
    def __init__(self,book_repository) -> None:
        self.book_repository = book_repository

    def add_new_book(self,id,title,author):
        # Business logic validation
        if not title or not author:
            raise ValueError("Title and author are required")

        book = Book(id,title,author)
        self.book_repository.add_book(book)
        return book

    def get_book_details(self,book_id):
        book = self.book_repository.get_book(book_id)
        if not book:
            raise ValueError("Book not found")
        return book

    def get_available_books(self):
        all_books = self.book_repository.get_all_book()
        return [book for book in all_books if book.is_available]


# --------------
# 4. Presentation Layer (UI Layer)
# Handles user interaction

class LibraryConsoleUI:
    def __init__(self,library_service,book_repository=None) -> None:
        self.library_service = library_service
        self.book_repository = book_repository

    def display_menu(self):
        print("\n=== Library Management System ===")
        print("0. Urgently add new book")
        print("1. Add new book")
        print("2. View book details")
        print("3. View all available books")
        print("4. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (0-4): ")
            
            if choice=="0":
                self.urgent_add_book_ui()
            elif choice == "1":
                self.add_book_ui()
            elif choice == "2":
                self.view_book_ui()
            elif choice == "3":
                self.view_available_books_ui()
            elif choice == "4":
                print("Goodbye!")
                break

    def add_book_ui(self):
        try:
            id = input("Enter book ID: ")
            title = input("Enter book title: ")
            author = input("Enter book author: ")

            book = self.library_service.add_new_book(id,title,author)
            print(f"Successfully added : {book}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def urgent_add_book_ui(self):
        if self.book_repository == None:
            raise ValueError("book can not be added as db layer not provided")
        try:
            id = input("Enter book ID: ")
            title = input("Enter book title: ")
            author = input("Enter book author ")
            book = Book(id,title,author)
            self.book_repository.add_book(book)
        except ValueError as e:
            print(f"Error : {e}")

    def view_book_ui(self):
        try:
            id = input("Enter book ID:")
            book = self.library_service.get_book_details(id)
            print(f"Book details: {book}")
        except ValueError as e:
            print(f"Error: {e}")

    def view_available_books_ui(self):
        books = self.library_service.get_available_books()
        if not books:
            print("No books available")
        else:
            print("Available books:")
            for book in books:
                print(book)



def main():
    #Initializa all layers
    book_repository = BookRepository()
    library_service = LibraryServices(book_repository)
    # passing the data layer (i.e. book repository) directly to the
    # presentation layer (i.e ui) helps us bypass services layer hence 
    # simulating a open layer in layered arcitecture 
    ui = LibraryConsoleUI(library_service)

    ui.run()

if __name__=='__main__':
    main()