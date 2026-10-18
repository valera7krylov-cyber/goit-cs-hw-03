
from pymongo import MongoClient
from pymongo.errors import PyMongoError

client = MongoClient("mongodb://localhost:27017/")

db = client["cats_database"]
cats = db["cats"]

def show_all_cats():
    """Print all cats from the collection."""
    for cat in cats.find():
        print(cat)


def find_cat_by_name(name):
    """Find and print a cat by its name."""
    cat = cats.find_one({"name": name})

    if cat:
        print(cat)
    else:
        print(f"Cat '{name}' was not found.")


def update_cat_age(name, age):
    """Update a cat's age by its name."""
    result = cats.update_one(
        {"name": name},
        {"$set": {"age": age}}
    )

    if result.matched_count:
        print(f"Age of '{name}' updated successfully.")
    else:
        print(f"Cat '{name}' was not found.")


def add_cat_feature(name, feature):
    """Add a new feature to a cat."""
    result = cats.update_one(
        {"name": name},
        {"$addToSet": {"features": feature}}
    )

    if result.matched_count:
        print(f"Feature added to '{name}'.")
    else:
        print(f"Cat '{name}' was not found.")


def delete_cat_by_name(name):
    """Delete a cat by its name."""
    result = cats.delete_one({"name": name})

    if result.deleted_count:
        print(f"Cat '{name}' deleted successfully.")
    else:
        print(f"Cat '{name}' was not found.")


def delete_all_cats():
    """Delete all cats from the collection."""
    result = cats.delete_many({})
    print(f"Deleted {result.deleted_count} cats.")



def main():
    """Run the interactive cats management menu."""
    if cats.count_documents({}) == 0:
        cats.insert_many([
            {
                "name": "barsik",
                "age": 3,
                "features": [
                    "ходит в тапки",
                    "даёт себя гладить",
                    "рыжий"
                ]
            },
            {
                "name": "murzik",
                "age": 5,
                "features": [
                    "любит спать",
                    "игривый"
                ]
            }
        ])
        print("Initial cats added to the database.")

    while True:
        print("\n--- Cats Management ---")
        print("1. Show all cats")
        print("2. Find a cat by name")
        print("3. Update a cat's age")
        print("4. Add a feature to a cat")
        print("5. Delete a cat")
        print("6. Delete all cats")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice not in {"0", "1", "2", "3", "4", "5", "6"}:
            print("Invalid option. Please try again.")
            continue

        try:
            if choice == "1":
                show_all_cats()

            elif choice == "2":
                name = input("Enter cat name: ")
                find_cat_by_name(name)

            elif choice == "3":
                name = input("Enter cat name: ")
                try:
                    age = int(input("Enter new age: "))
                    if age < 0:
                        print("Age cannot be negative.")
                        continue
                    update_cat_age(name, age)
                except ValueError:
                    print("Age must be an integer.")

            elif choice == "4":
                name = input("Enter cat name: ")
                feature = input("Enter new feature: ")
                add_cat_feature(name, feature)

            elif choice == "5":
                name = input("Enter cat name: ")
                delete_cat_by_name(name)

            elif choice == "6":
                confirm = input("Delete ALL cats? Type yes to confirm: ")
                if confirm.lower() == "yes":
                    delete_all_cats()
                else:
                    print("Deletion cancelled.")

            elif choice == "0":
                print("Goodbye!")
                break

        except PyMongoError as error:
            print(f"Database operation failed: {error}")


try:
    client.admin.command("ping")
    print("Connected to MongoDB successfully!")
    main()

except PyMongoError as error:
    print(f"Database error: {error}")

finally:
    client.close()

