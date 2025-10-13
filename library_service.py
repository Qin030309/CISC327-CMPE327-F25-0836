"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_patron_borrow_count,
    insert_book, insert_borrow_record, update_book_availability,
    update_borrow_record_return_date, get_all_books,
    get_patron_borrowed_books  # <-- 加这一行
)

def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    if len(isbn) != 13:
        return False, "ISBN must be exactly 13 digits."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    success = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if success:
        return True, f'Book "{title.strip()}" has been successfully added to the catalog.'
    else:
        return False, "Database error occurred while adding the book."

def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."
    
    # Check patron's current borrowed books count
    current_borrowed = get_patron_borrow_count(patron_id)
    
    if current_borrowed > 5:
        return False, "You have reached the maximum borrowing limit of 5 books."
    
    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    # Insert borrow record and update availability
    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."
    
    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'

def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Process book return by a patron.
    
    TODO: Implement R4 as per requirements
    
    """
    """
    R4: Book Return Processing

    Steps:
    1. Validate patron ID format
    2. Check if book exists
    3. Verify that this patron borrowed this book and not yet returned
    4. Update return date
    5. Update book availability (+1)
    6. Calculate and report late fee using R5
    """

    # Step 1: Validate patron ID
    if not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be a 6-digit number."

    # Step 2: Validate that the book exists
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book return functionality is not yet implemented."

    # Step 3: Verify that this patron actually borrowed this book and not yet returned
    borrowed_books = get_patron_borrowed_books(patron_id)
    borrowed_book = None
    for b in borrowed_books:
        if b["book_id"] == book_id and b["return_date"] is None:
            borrowed_book = b
            break

    if not borrowed_book:
        return False, "No active borrow record found for this patron and book."

    # Step 4: Update the borrow record with the return date
    return_date = datetime.now()
    success = update_borrow_record_return_date(patron_id, book_id, return_date)
    if not success:
        return False, "Database error occurred while updating return record."

    # Step 5: Increment available copies
    availability_success = update_book_availability(book_id, +1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."

    # Step 6: Calculate late fee (use R5)
    fee_info = calculate_late_fee_for_book(patron_id, book_id)
    fee = fee_info.get("fee_amount", 0.00)
    days = fee_info.get("days_overdue", 0)

    # Step 7: Return user-friendly message
    if fee > 0:
        return True, f'Book "{book["title"]}" returned successfully. Late fee: ${fee:.2f} ({days} day(s) overdue).'
    else:
        return True, f'Book "{book["title"]}" returned successfully. No late fee.'

            
def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    """
    Calculate late fees for a specific book.
    
    TODO: Implement R5 as per requirements 
    
    
    return { // return the calculated values
        'fee_amount': 0.00,
        'days_overdue': 0,
        'status': 'Late fee calculation not implemented'
    }
    """
    borrowed_books = get_patron_borrowed_books(patron_id)
    
    # Find the specific borrowed book
    borrowed_book = None
    for b in borrowed_books:
       if b["book_id"] == book_id and b["return_date"] is None:
          borrowed_book = b
          break
    if not borrowed_book:
       return {
            "fee_amount": 0.00,
            "days_overdue": 0,
            "status": "No active borrow record found for this patron and book"
        }
    due_date = borrowed_book["due_date"]
    now = datetime.now()
    if now <= due_date:
                return {
            "fee_amount": 0.00,
            "days_overdue": 0,
            "status": "Book is not overdue"
        }
    # Calculate days overdue
    days_overdue = (now - due_date).days
    # Calculate fee according to R5 rules
    first_7_days = min(days_overdue, 7)
    additional_days = max(days_overdue - 7, 0)
    fee = first_7_days * 0.50 + additional_days * 1.00     
    fee = min(fee, 15.00)  # cap at $15
    return {
        "fee_amount": round(fee, 2),
        "days_overdue": days_overdue,
        "status": "Late fee calculated successfully"
    }
    
def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """
    R6: Book Search Functionality
    
    Search for books in the catalog based on:
    - search_type: "title", "author", "isbn"
    - partial match for title/author (case-insensitive)
    - exact match for ISBN
    """
    search_term = search_term.strip()
    if not search_term:
        return []

    all_books = get_all_books()
    results = []

    if search_type.lower() == "title":
        for book in all_books:
            if search_term.lower() in book["title"].lower():
                results.append(book)
    elif search_type.lower() == "author":
        for book in all_books:
            if search_term.lower() in book["author"].lower():
                results.append(book)
    elif search_type.lower() == "isbn":
        for book in all_books:
            if search_term == book["isbn"]:
                results.append(book)
    else:
        # Invalid search_type, return empty
        return []

    return results


def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.
    
    TODO: Implement R7 as per requirements
    """
    report = {
        "patron_id": patron_id,
        "current_borrowed": [],
        "total_late_fees": 0.00,
        "num_currently_borrowed": 0,
        "borrow_history": []
    }
    borrowed_books = get_patron_borrowed_books(patron_id)
    for book in borrowed_books:
             # Add current borrowed book info
        if book["return_date"] is None:
            fee_info = calculate_late_fee_for_book(patron_id, book["book_id"])
            report["current_borrowed"].append({
                "book_id": book["book_id"],
                "title": book["title"],
                "author": book["author"],
                "borrow_date": book["borrow_date"],
                "due_date": book["due_date"],
                "late_fee": fee_info.get("fee_amount", 0.00)
            })
            report["total_late_fees"] += fee_info.get("fee_amount", 0.00)
            report["num_currently_borrowed"] += 1
        
        # Add to borrow history
        report["borrow_history"].append({
            "book_id": book["book_id"],
            "title": book["title"],
            "author": book["author"],
            "borrow_date": book["borrow_date"],
            "due_date": book["due_date"],
            "return_date": book["return_date"],
            "late_fee": calculate_late_fee_for_book(patron_id, book["book_id"]).get("fee_amount", 0.00)
        })
    
    # Round total late fees
    report["total_late_fees"] = round(report["total_late_fees"], 2)
    
    return report
