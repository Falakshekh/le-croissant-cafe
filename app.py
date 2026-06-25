import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from AI import ai_menu_suggestor, train_and_predict_occupancy

app = Flask(__name__)
CORS(app)

# 1. PAGES ROUTES
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/bookings')
def view_bookings():
    return render_template('bookings.html')


# 2. API: AI MENU SEARCH
@app.route('/api/search', methods=['POST'])
def search_api():
    data = request.json
    user_msg = data.get('message', '')
    raw_suggestions = ai_menu_suggestor(user_msg)
    
    formatted_data = []
    for item in raw_suggestions:
        formatted_data.append({
            "name": item[0],
            "price": item[1],
            "description": item[2]
        })
    return jsonify({"status": "success", "data": formatted_data})


# 3. API: SEAT BOOKING TRANSACTION (SQL)
@app.route('/api/book', methods=['POST'])
def book_api():
    data = request.json
    name = data.get('name')
    seat = data.get('seat')
    date = data.get('date')
    time = data.get('time')
    
    if not all([name, seat, date, time]):
        return jsonify({"status": "error", "message": "Missing fields"}), 400
        
    conn = sqlite3.connect('cafe_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (customer_name, seat_number, booking_date, booking_time) VALUES (?, ?, ?, ?)",
                   (name, seat, date, time))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Booking recorded!"})


# 4. API: CUSTOMER ORDER & RATING TRANSACTION (SQL)
@app.route('/api/order-rating', methods=['POST'])
def order_rating_api():
    data = request.json
    name = data.get('name')
    items = data.get('items')
    rating = data.get('rating')
    checkout = data.get('checkout') # Kab gaya data
    
    if not all([name, items, rating, checkout]):
        return jsonify({"status": "error", "message": "All fields required"}), 400
        
    conn = sqlite3.connect('cafe_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (customer_name, order_items, rating, check_out_time) VALUES (?, ?, ?, ?)",
                   (name, items, int(rating), checkout))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Order & Rating saved securely!"})


# 5. API: ML OCCUPANCY PREDICTOR
@app.route('/api/predict-seat', methods=['POST'])
def predict_api():
    data = request.json
    date_str = data.get('date', '')
    prediction_text = train_and_predict_occupancy(date_str)
    return jsonify({"status": "success", "prediction": prediction_text})


# 6. API: SECURE OWNER DASHBOARD REALDATA (SQL Fetch)
@app.route('/api/admin/dashboard', methods=['GET'])
def admin_dashboard_api():
    conn = sqlite3.connect('cafe_database.db')
    cursor = conn.cursor()
    
    # Fetch Bookings data (Kon Aaya)
    cursor.execute("SELECT id, customer_name, seat_number, booking_date, booking_time FROM bookings ORDER BY id DESC")
    bookings = cursor.fetchall()
    
    # Fetch Orders, Ratings & Checkout data (Kya khaya, Kab gya, Rating)
    cursor.execute("SELECT id, customer_name, order_items, rating, check_out_time FROM orders ORDER BY id DESC")
    orders = cursor.fetchall()
    
    conn.close()
    return jsonify({
        "status": "success",
        "bookings": bookings,
        "orders": orders
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)