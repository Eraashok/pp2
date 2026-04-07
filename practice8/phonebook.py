from connect import connect


def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL
    );
    """
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
    print("Table phonebook is ready.")


def search_contacts():
    pattern = input("Enter pattern to search (name/phone): ").strip()

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
            rows = cur.fetchall()

            if rows:
                print("\nSearch results:")
                for row in rows:
                    print(row)
            else:
                print("No contacts found.")


def upsert_contact():
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL upsert_contact(%s, %s)",
                (name, phone)
            )
        conn.commit()

    print("Contact inserted/updated successfully.")


def bulk_insert():
    n = int(input("How many contacts do you want to add? "))

    names = []
    phones = []

    for i in range(n):
        print(f"\nContact {i+1}")
        names.append(input("Name: ").strip())
        phones.append(input("Phone: ").strip())

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CALL insert_many_contacts(%s, %s)",
                (names, phones)
            )
        conn.commit()

    print("Bulk insert completed.")
    print("Check incorrect_contacts table for invalid data.")


def show_paginated():
    limit = int(input("Enter LIMIT: "))
    offset = int(input("Enter OFFSET: "))

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_paginated(%s, %s)",
                (limit, offset)
            )
            rows = cur.fetchall()

            if rows:
                print("\nPaginated results:")
                for row in rows:
                    print(row)
            else:
                print("No data found.")


def delete_contact():
    value = input("Enter username or phone to delete: ").strip()

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_contact(%s)", (value,))
        conn.commit()

    print("Contact(s) deleted if matched.")


def show_incorrect_contacts():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, phone, error_message, created_at
                FROM incorrect_contacts
                ORDER BY id
            """)
            rows = cur.fetchall()

            if rows:
                print("\nIncorrect contacts:")
                for row in rows:
                    print(row)
            else:
                print("No incorrect contacts found.")


def show_all_contacts():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, phone
                FROM phonebook
                ORDER BY id
            """)
            rows = cur.fetchall()

            if rows:
                print("\nAll contacts:")
                for row in rows:
                    print(row)
            else:
                print("Phonebook is empty.")


def menu():
    while True:
        print("\n=== PHONEBOOK MENU ===")
        print("1. Create table")
        print("2. Search contacts by pattern")
        print("3. Insert or update contact")
        print("4. Bulk insert contacts")
        print("5. Show contacts with pagination")
        print("6. Delete contact by username or phone")
        print("7. Show all contacts")
        print("8. Show incorrect contacts")
        print("9. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_table()
        elif choice == "2":
            search_contacts()
        elif choice == "3":
            upsert_contact()
        elif choice == "4":
            bulk_insert()
        elif choice == "5":
            show_paginated()
        elif choice == "6":
            delete_contact()
        elif choice == "7":
            show_all_contacts()
        elif choice == "8":
            show_incorrect_contacts()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    menu()