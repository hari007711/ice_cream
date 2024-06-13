import sqlite3

def connect_db():
    try:
        # Connect to an in-memory database
        return sqlite3.connect(':memory:')
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table_allergens(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS allergens (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
    )
    ''')

def create_ingredients_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
    ''')

def create_suggestions_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS suggestions (
        id INTEGER PRIMARY KEY,
        customer_name TEXT NOT NULL,
        flavor_suggestion TEXT NOT NULL,
        allergy_concerns TEXT
    )
    ''')

def create_seasonal_flavor_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS seasonal_flavors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        ingredients TEXT
    )
    ''')

def create_tables(cursor):
    create_table_allergens(cursor)
    create_ingredients_table(cursor)
    create_suggestions_table(cursor)
    create_seasonal_flavor_table(cursor)

def add_seasonal_flavor(cursor, name, description, ingredients):
    cursor.execute('''
    INSERT INTO seasonal_flavors (name, description, ingredients)
    VALUES (?, ?, ?)
    ''', (name, description, ingredients))
    print("Seasonal flavor added successfully.")

def add_ingredient(cursor, name, quantity):
    cursor.execute('''
    INSERT INTO ingredients (name, quantity)
    VALUES (?, ?)
    ''', (name, quantity))
    print("Ingredient added successfully.")

def add_suggestion(cursor, customer_name, flavor_suggestion, allergy_concerns):
    cursor.execute('''
    INSERT INTO suggestions (customer_name, flavor_suggestion, allergy_concerns)
    VALUES (?, ?, ?)
    ''', (customer_name, flavor_suggestion, allergy_concerns))
    print("Suggestion added successfully.")

def add_allergen(cursor, allergen):
    cursor.execute('''
    INSERT INTO allergens (name, description) VALUES (?, ?)
    ''', (allergen['name'], allergen['description']))
    print("Allergen added successfully.")

def list_seasonal_flavors(cursor):
    cursor.execute('SELECT * FROM seasonal_flavors')
    flavors = cursor.fetchall()
    return flavors

def search_flavors(cursor, keyword):
    sql_query = '''
    SELECT * FROM seasonal_flavors
    WHERE name LIKE ? OR description LIKE ?
    '''
    cursor.execute(sql_query, (f'%{keyword}%', f'%{keyword}%'))
    results = cursor.fetchall()
    return results

def main():
    conn = connect_db()
    if conn is not None:
        cursor = conn.cursor()
        create_tables(cursor)
        cart = []
        while True:
            print("\nIce Cream Parlor Cafe")
            print("1. List Seasonal Flavors")
            print("2. Search Flavors")
            print("3. Add Ingredient")
            print("4. Add Customer Suggestion")
            print("5. Add Allergen")
            print("6. Add Flavor to Cart")
            print("7. View Cart")
            print("8. Add Seasonal Flavor")
            print("9. Exit")
            
            choice = input("Enter your choice: ")

            if choice == '1':
                flavors = list_seasonal_flavors(cursor)
                for flavor in flavors:
                    print(f"ID: {flavor[0]}, Name: {flavor[1]}, Description: {flavor[2]}, Ingredients: {flavor[3]}")
            elif choice == '2':
                keyword = input("Enter keyword to search: ")
                results = search_flavors(cursor, keyword)
                for result in results:
                    print(f"ID: {result[0]}, Name: {result[1]}, Description: {result[2]}, Ingredients: {result[3]}")
            elif choice == '3':
                name = input("Enter ingredient name: ")
                quantity = int(input("Enter ingredient quantity: "))
                add_ingredient(cursor, name, quantity)
            elif choice == '4':
                customer_name = input("Enter your name: ")
                flavor_suggestion = input("Enter flavor suggestion: ")
                allergy_concerns = input("Enter any allergy concerns: ")
                add_suggestion(cursor, customer_name, flavor_suggestion, allergy_concerns)
            elif choice == '5':
                name = input("Enter allergen name: ")
                description = input("Enter allergen description: ")
                add_allergen(cursor, {'name': name, 'description': description})
            elif choice == '6':
                flavor_id = input("Enter flavor ID to add to cart: ")
                cart.append(flavor_id)
                print(f"Flavor ID {flavor_id} added to cart. Current cart: {cart}")
            elif choice == '7':
                print("Your Cart:", cart)
            elif choice == '8':
                seasonal_flavor_name = input("Enter flavor name: ")
                flavor_description = input("Enter flavor description: ")
                flavor_ingredients = input("Enter flavor ingredients: ")
                add_seasonal_flavor(cursor, seasonal_flavor_name, flavor_description, flavor_ingredients)
            elif choice == '9':
                break
            else:
                print("Invalid choice. Please try again.")

            conn.commit()

        conn.close()
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()
