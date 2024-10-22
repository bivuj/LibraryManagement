import mysql.connector
from datetime import datetime

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="365Pass",
    database="library_db"
)

cursor = db.cursor()


def add_book(title, author, copies):
    query = "INSERT INTO books (title, author, copies) VALUES (%s, %s, %s)"
    values = (title, author, copies)
    cursor.execute(query, values)
    db.commit()
    print(f"Book '{title}' added successfully!")


def view_books():
    query = "SELECT * FROM books"
    cursor.execute(query)
    results = cursor.fetchall()

    if results:
        print("Available Books:")
        for row in results:
            print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Copies: {row[3]}")
    else:
        print("No books available.")


def issue_book(book_id, issued_to):
    query = "SELECT copies FROM books WHERE id = %s"
    cursor.execute(query, (book_id,))
    result = cursor.fetchone()

    if result and result[0] > 0:
        query = "INSERT INTO issued_books (book_id, issued_to, issue_date) VALUES (%s, %s, %s)"
        values = (book_id, issued_to, datetime.now().date())
        cursor.execute(query, values)

        query = "UPDATE books SET copies = copies - 1 WHERE id = %s"
        cursor.execute(query, (book_id,))
        db.commit()
        print(f"Book ID {book_id} issued to {issued_to}.")
    else:
        print("Book not available for issue.")


def return_book(issue_id):
    query = "SELECT book_id FROM issued_books WHERE id = %s"
    cursor.execute(query, (issue_id,))
    result = cursor.fetchone()

    if result:
        query = "UPDATE books SET copies = copies + 1 WHERE id = %s"
        cursor.execute(query, (result[0],))

        query = "UPDATE issued_books SET return_date = %s WHERE id = %s"
        cursor.execute(query, (datetime.now().date(), issue_id))
        db.commit()
        print(f"Issue ID {issue_id} returned successfully!")
    else:
        print("Invalid issue ID.")


def main():
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. View Books")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            copies = int(input("Enter number of copies: "))
            add_book(title, author, copies)

        elif choice == '2':
            view_books()

        elif choice == '3':
            book_id = int(input("Enter book ID to issue: "))
            issued_to = input("Enter the name of the person: ")
            issue_book(book_id, issued_to)

        elif choice == '4':
            issue_id = int(input("Enter issue ID to return: "))
            return_book(issue_id)

        elif choice == '5':
            print("Exiting the system.")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
