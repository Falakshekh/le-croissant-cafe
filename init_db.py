import sqlite3

def init_db():
    conn = sqlite3.connect('cafe_database.db')
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT DEFAULT 'customer'
    )''')

    # 2. Menu Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        description TEXT,
        tags TEXT
    )''')

    # 3. Bookings Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        seat_number INTEGER NOT NULL,
        booking_date TEXT NOT NULL,
        booking_time TEXT NOT NULL
    )''')

    # 4. Orders & Ratings Table (Fixed Columns to Match Form and Dashboard)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        items_ordered TEXT NOT NULL,
        rating INTEGER DEFAULT 0,
        check_out_time TEXT NOT NULL
    )''')

    cursor.execute("SELECT COUNT(*) FROM menu")
    if cursor.fetchone()[0] == 0:
        menu_items = [
            ('Crisp Berry Croissant', 'bakery', 250.00, 
            'Laminated crisp croissant with wild berry core. Heavy and thick fruity filling.', 
            'sweet, berry, bakery, crisp, heavy, mitha, meetha, thick'),
        
            ('Black Forest Ornament', 'dessert', 320.00, 
            'Artisan chocolate dessert ball with creamy rich cocoa layer.', 
            'sweet, chocolate, dessert, creamy, dark, mitha, meetha, heavy'),
        
            ('Pumpkin Matcha Latte', 'drinks', 180.00, 
            'Cinnamon flavored cold matcha latte with thick creamy foam top.', 
            'cold, bitter, sweet, cinnamon, latte, matcha, thick, creamy, chilled, thanda'),
        
             ('Caramel Pear Dessert', 'dessert', 290.00, 
            'Caramelized pear with hazelnut, heavy sweet topping.', 
            'sweet, caramel, dessert, heavy, mitha, meetha'),
        
            ('Iced Cold Coffee', 'drinks', 150.00, 
            'Chilled creamy coffee, thick texture served with ice blend.', 
             'cold, coffee, sweet, thick, creamy, ice, chilled, thanda, shake')
        ]

        cursor.executemany("INSERT INTO menu (item_name, category, price, description, tags) VALUES (?, ?, ?, ?, ?)", menu_items)
        print("Menu items inserted successfully!")

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()

