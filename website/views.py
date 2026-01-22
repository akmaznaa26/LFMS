from datetime import datetime, date, timedelta  # remove 'time' from here
import time  # standard Python time module
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from urllib3 import request
from .models import Profile, Book, Borrow, Staff, Payment
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.db import connection
from django.conf import settings
import os


# Home page
def home(request):
    return render(request, "website/home.html")


# Profile (login required)
@login_required
def profile(request):
    return render(request, "website/profile.html")


# About page
def about(request):
    return render(request, "website/about.html")


# Book page
@login_required
def book(request):

    # ================= DATABASE PATH =================
    db_path = os.path.join(settings.BASE_DIR, "main.db")

    # ================= ADD / UPDATE =================
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        title = request.POST.get("title")
        author = request.POST.get("author")
        isbn = request.POST.get("isbn")
        price = request.POST.get("price")
        status = request.POST.get("status")

        with connection.cursor() as cursor:
            cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")

            if book_id:  # UPDATE
                cursor.execute(
                    """
                    UPDATE external_db.books
                    SET Title=%s, Author=%s, ISBN=%s, Price=%s, Status=%s
                    WHERE Book_id=%s
                """,
                    [title, author, isbn, price, status, book_id],
                )
            else:  # ADD
                cursor.execute(
                    """
                    INSERT INTO external_db.books
                    (Title, Author, ISBN, Price, Status)
                    VALUES (%s, %s, %s, %s, %s)
                """,
                    [title, author, isbn, price, status],
                )

            cursor.execute("DETACH DATABASE external_db")

        return redirect("book")

    # ================= DELETE =================
    delete_id = request.GET.get("delete")
    if delete_id:
        with connection.cursor() as cursor:
            cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")
            cursor.execute(
                "DELETE FROM external_db.books WHERE Book_id = %s", [delete_id]
            )
            cursor.execute("DETACH DATABASE external_db")
        return redirect("book")

    # ================= EDIT (GET ONE BOOK) =================
    edit_id = request.GET.get("edit")
    edit_book = None
    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")
            cursor.execute(
                """
                SELECT Book_id, Title, Author, ISBN, Price, Status
                FROM external_db.books
                WHERE Book_id = %s
            """,
                [edit_id],
            )
            row = cursor.fetchone()
            cursor.execute("DETACH DATABASE external_db")

        if row:
            edit_book = {
                "book_id": row[0],
                "title": row[1],
                "author": row[2],
                "isbn": row[3],
                "price": row[4],
                "status": row[5],
            }

    # ================= DISPLAY ALL BOOKS =================
    with connection.cursor() as cursor:
        cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")
        cursor.execute(
            """
            SELECT Book_id, Title, Author, ISBN, Price, Status
            FROM external_db.books
        """
        )
        rows = cursor.fetchall()
        cursor.execute("DETACH DATABASE external_db")

    books = []
    for r in rows:
        books.append(
            {
                "book_id": r[0],
                "title": r[1],
                "author": r[2],
                "isbn": r[3],
                "price": r[4],
                "status": r[5],
            }
        )

    # ================= CONTEXT =================
    context = {
        "books": books,
        "edit": edit_book,
    }

    return render(request, "website/book.html", context)


# Staff page
@login_required
def staff(request):

    # ================= DATABASE PATH =================
    db_path = os.path.join(settings.BASE_DIR, "main.db")

    # ================= ADD / UPDATE =================
    if request.method == "POST":
        staff_id = request.POST.get("staff_id")
        staff_name = request.POST.get("staff_name")
        assigning_section = request.POST.get("assigning_section")
        staff_email = request.POST.get("staff_email")
        shift = request.POST.get("shift")

        with connection.cursor() as cursor:
            cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")

            if staff_id:  # UPDATE
                cursor.execute(
                    """
                    UPDATE external_db.staffs
                    SET Staff_name=%s,
                        Assigning_section=%s,
                        Staff_email=%s,
                        "Shift"=%s
                    WHERE Staff_id=%s
                """,
                    [staff_name, assigning_section, staff_email, shift, staff_id],
                )
            else:  # ADD
                cursor.execute(
                    """
                    INSERT INTO external_db.staffs
                    (Staff_name, Assigning_section, Staff_email, "Shift")
                    VALUES (%s, %s, %s, %s)
                """,
                    [staff_name, assigning_section, staff_email, shift],
                )

            cursor.execute("DETACH DATABASE external_db")

        return redirect("staff")

    # ================= DELETE =================
    delete_id = request.GET.get("delete")
    if delete_id:
        with connection.cursor() as cursor:
            cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")
            cursor.execute(
                "DELETE FROM external_db.staffs WHERE Staff_id=%s", [delete_id]
            )
            cursor.execute("DETACH DATABASE external_db")
        return redirect("staff")

    # ================= EDIT (GET ONE STAFF) =================
    edit_id = request.GET.get("edit")
    edit_staff = None
    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")
            cursor.execute(
                """
                SELECT Staff_id, Staff_name, Assigning_section,
                       Staff_email, "Shift"
                FROM external_db.staffs
                WHERE Staff_id=%s
            """,
                [edit_id],
            )
            row = cursor.fetchone()
            cursor.execute("DETACH DATABASE external_db")

        if row:
            edit_staff = {
                "staff_id": row[0],
                "staff_name": row[1],
                "assigning_section": row[2],
                "staff_email": row[3],
                "shift": row[4],
            }

    # ================= DISPLAY ALL STAFF =================
    with connection.cursor() as cursor:
        cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")
        cursor.execute(
            """
            SELECT Staff_id, Staff_name, Assigning_section,
                   Staff_email, "Shift"
            FROM external_db.staffs
            ORDER BY Staff_id DESC
        """
        )
        rows = cursor.fetchall()
        cursor.execute("DETACH DATABASE external_db")

    staffs = []
    for r in rows:
        staffs.append(
            {
                "staff_id": r[0],
                "staff_name": r[1],
                "assigning_section": r[2],
                "staff_email": r[3],
                "shift": r[4],
            }
        )

    # ================= CONTEXT =================
    context = {
        "staffs": staffs,
        "edit": edit_staff,
    }

    return render(request, "website/staff.html", context)


# Help page
@login_required
def help(request):
    return render(request, "website/help.html")


# User page
@login_required
def user(request):
    db_path = os.path.join(settings.BASE_DIR, "main.db")
    LIMIT_DAYS = 2
    FINE_PER_DAY = 1

    # ================= ADD / UPDATE =================
    if request.method == "POST":
        borrow_id = request.POST.get("borrow_id")  # rowid
        username = request.POST.get("username")
        book_id = int(request.POST.get("book_id") or 0)  # cast to int
        title = request.POST.get("title")
        borrow_date_str = request.POST.get("borrow_date")
        return_date_str = request.POST.get("return_date")

        if not borrow_date_str:
            return redirect("user")

        borrow_date = datetime.strptime(borrow_date_str, "%Y-%m-%d").date()
        return_date = (
            datetime.strptime(return_date_str, "%Y-%m-%d").date()
            if return_date_str
            else None
        )

        due_date = borrow_date + timedelta(days=LIMIT_DAYS)
        today = date.today()

        if return_date:
            late_days = (return_date - due_date).days
        else:
            late_days = (today - due_date).days

        late_days = max(0, late_days)
        late_days = int(late_days)  # cast to int
        fine_amounts = int(late_days * FINE_PER_DAY)  # cast to int

        with connection.cursor() as cursor:
            cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")

            if borrow_id:  # UPDATE
                cursor.execute(
                    """
                    UPDATE external_db.borrow
                    SET Username=%s,
                        Book_id=%s,
                        Title=%s,
                        Borrow_date=%s,
                        Return_date=%s,
                        Late_days=%s,
                        Fine_amounts=%s
                    WHERE rowid=%s
                """,
                    [
                        username,
                        book_id,
                        title,
                        borrow_date_str,
                        return_date_str,
                        late_days,
                        fine_amounts,
                        borrow_id,
                    ],
                )
            else:  # ADD
                cursor.execute(
                    """
                    INSERT INTO external_db.borrow
                    (Username, Book_id, Title, Borrow_date, Return_date, Late_days, Fine_amounts)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                    [
                        username,
                        book_id,
                        title,
                        borrow_date_str,
                        return_date_str,
                        late_days,
                        fine_amounts,
                    ],
                )

            cursor.execute("DETACH DATABASE external_db")

        return redirect("user")

    # ================= DELETE =================
    delete_id = request.GET.get("delete")
    if delete_id:
        with connection.cursor() as cursor:
            cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")
            cursor.execute("DELETE FROM external_db.borrow WHERE rowid=%s", [delete_id])
            cursor.execute("DETACH DATABASE external_db")
        return redirect("user")

    # ================= AUTO UPDATE FINE =================
    today = date.today()
    with connection.cursor() as cursor:
        cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")
        cursor.execute(
            """
            SELECT rowid, Borrow_date, Return_date
            FROM external_db.borrow
        """
        )
        rows = cursor.fetchall()

        for r in rows:
            rid = r[0]
            borrow_date = datetime.strptime(r[1], "%Y-%m-%d").date()
            return_date = datetime.strptime(r[2], "%Y-%m-%d").date() if r[2] else None

            due_date = borrow_date + timedelta(days=LIMIT_DAYS)

            if return_date:
                late_days = (return_date - due_date).days
            else:
                late_days = (today - due_date).days

            late_days = max(0, late_days)
            late_days = int(late_days)
            fine_amounts = int(late_days * FINE_PER_DAY)

            cursor.execute(
                """
                UPDATE external_db.borrow
                SET Late_days=%s,
                    Fine_amounts=%s
                WHERE rowid=%s
            """,
                [late_days, fine_amounts, rid],
            )

        cursor.execute("DETACH DATABASE external_db")

    # ================= EDIT =================
    edit_id = request.GET.get("edit")
    edit_borrow = None
    if edit_id:
        with connection.cursor() as cursor:
            cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")
            cursor.execute(
                """
                SELECT rowid, Username, Book_id, Title,
                       Borrow_date, Return_date, Late_days, Fine_amounts
                FROM external_db.borrow
                WHERE rowid=%s
            """,
                [edit_id],
            )
            row = cursor.fetchone()
            cursor.execute("DETACH DATABASE external_db")

        if row:
            edit_borrow = {
                "borrow_id": row[0],
                "username": row[1],
                "book_id": int(row[2]),
                "title": row[3],
                "borrow_date": row[4],
                "return_date": row[5],
                "late_days": int(row[6]),
                "fine_amounts": int(row[7]),
            }

    # ================= DISPLAY =================
    with connection.cursor() as cursor:
        cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")
        cursor.execute(
            """
            SELECT rowid, Username, Book_id, Title,
                   Borrow_date, Return_date, Late_days, Fine_amounts
            FROM external_db.borrow
            ORDER BY rowid DESC
        """
        )
        rows = cursor.fetchall()
        cursor.execute("DETACH DATABASE external_db")

    borrows = []
    for r in rows:
        borrows.append(
            {
                "borrow_id": r[0],
                "username": r[1],
                "book_id": int(r[2]),
                "title": r[3],
                "borrow_date": r[4],
                "return_date": r[5],
                "late_days": int(r[6]),
                "fine_amounts": int(r[7]),
            }
        )

    context = {
        "borrows": borrows,
        "edit": edit_borrow,
    }

    return render(request, "website/user.html", context)


# ===============================
# ROLE REDIRECT (AFTER LOGIN)
# ===============================
@login_required
def role_redirect(request):
    role = request.user.profile.role

    if role in ["admin", "staff"]:
        return redirect("staff")
    elif role == "user":
        return redirect("user")
    elif role == "bank":
        return redirect("payment")
    return redirect("home")


def admin(request):
    return render(request, "website/admin.html")


# BANK
def bank(request):
    db_path = os.path.join(settings.BASE_DIR, "main.db")

    # ================= GET PAYMENTS =================
    payments = []
    with connection.cursor() as cursor:
        cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")
        cursor.execute(
            """
            SELECT rowid, name, card_number, borrow_id, fine_amount, payment_date
            FROM external_db.bank
            ORDER BY rowid DESC
            """
        )
        rows = cursor.fetchall()
        cursor.execute("DETACH DATABASE external_db")

    for r in rows:
        payments.append(
            {
                "rowid": r[0],
                "name": r[1],
                "card_number": r[2],
                "borrow_id": int(r[3]) if r[3] is not None else 0,
                "fine_amount": float(r[4]) if r[4] is not None else 0,
                "payment_date": (
                    datetime.strptime(r[5], "%Y-%m-%d %H:%M:%S") if r[5] else None
                ),
            }
        )

    # ================= POST ACTION =================
    if request.method == "POST":
        action = request.POST.get("action")

        with connection.cursor() as cursor:
            cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")

            # ---------- PAY FINE ----------
            if action == "pay_fine":
                name = (request.POST.get("name") or "").strip()
                card_number = (request.POST.get("card_number") or "").strip()
                borrow_id_raw = request.POST.get("borrow_id")
                fine_amount_raw = request.POST.get("fine_amount")

                try:
                    borrow_id = int(borrow_id_raw) if borrow_id_raw else 0
                    fine_amount = float(fine_amount_raw) if fine_amount_raw else 0
                except ValueError:
                    messages.error(request, "Invalid borrow ID or fine amount.")
                    cursor.execute("DETACH DATABASE external_db")
                    return redirect("bank")

                if not name or not card_number:
                    messages.error(request, "Name and card number cannot be empty.")
                else:
                    payment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cursor.execute(
                        """
                        INSERT INTO external_db.bank
                        (name, card_number, borrow_id, fine_amount, payment_date)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        [
                            name,
                            card_number,
                            borrow_id,
                            fine_amount,
                            payment_date,
                        ],
                    )
                    messages.success(request, "Payment successful!")

            # ---------- DELETE PAYMENT ----------
            elif action == "delete_payment":
                rowid_raw = request.POST.get("payment_id")
                if rowid_raw:
                    try:
                        rowid = int(rowid_raw)
                        cursor.execute(
                            "DELETE FROM external_db.bank WHERE rowid=%s",
                            [rowid],
                        )
                        messages.success(request, "Payment deleted!")
                    except ValueError:
                        messages.error(request, "Invalid payment ID.")
                else:
                    messages.error(request, "Payment ID is missing!")

            cursor.execute("DETACH DATABASE external_db")

        return redirect("bank")  # prevent double POST

    return render(request, "website/bank.html", {"payments": payments})


from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
    return user.groups.filter(name="Admin").exists()


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, "admin/dashboard.html")


def book_list(request):
    # Initialize books in session
    if "books" not in request.session:
        request.session["books"] = []

    books = request.session["books"]

    # ================= DELETE =================
    book_id_to_delete = request.GET.get("delete")
    if book_id_to_delete:
        books = [b for b in books if str(b["book_id"]) != str(book_id_to_delete)]
        request.session["books"] = books
        return redirect("book")

    # ================= EDIT =================
    edit_id = request.GET.get("edit")
    edit_book = None
    if edit_id:
        for b in books:
            if str(b["book_id"]) == str(edit_id):
                edit_book = b
                break

    # ================= ADD / UPDATE =================
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        title = request.POST.get("title")
        author = request.POST.get("author")
        isbn = request.POST.get("isbn")
        price = request.POST.get("price")
        status = request.POST.get("status")

        if book_id:  # UPDATE existing
            for b in books:
                if str(b["book_id"]) == str(book_id):
                    b["title"] = title
                    b["author"] = author
                    b["isbn"] = isbn
                    b["price"] = price
                    b["status"] = status
                    break
        else:  # ADD new (auto ID)
            new_id = 1 if len(books) == 0 else max(b["book_id"] for b in books) + 1

            books.append(
                {
                    "book_id": new_id,
                    "title": title,
                    "author": author,
                    "isbn": isbn,
                    "price": price,
                    "status": status or "Available",
                }
            )

        request.session["books"] = books
        return redirect("book")

    context = {
        "books": books,
        "edit": edit_book,
    }
    return render(request, "website/book.html", context)


def list(request):
    db_path = os.path.join(settings.BASE_DIR, "main.db")

    with connection.cursor() as cursor:
        cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")
        cursor.execute(
            "SELECT Book_id, Title, Author, ISBN, Price, Status FROM external_db.books"
        )
        books = cursor.fetchall()
        cursor.execute("DETACH DATABASE external_db")

    return render(request, "website/list.html", {"books": books})


def data(request):
    db_path = os.path.join(settings.BASE_DIR, "main.db")

    with connection.cursor() as cursor:
        cursor.execute(f"ATTACH DATABASE '{db_path}' AS external_db")
        cursor.execute(
            """
            SELECT rowid, Username, Book_id, Title,
                   Borrow_date, Return_date, Late_days, Fine_amounts
            FROM external_db.borrow
            ORDER BY rowid DESC
            """
        )
        borrows = cursor.fetchall()
        cursor.execute("DETACH DATABASE external_db")

    return render(request, "website/data.html", {"borrows": borrows})
