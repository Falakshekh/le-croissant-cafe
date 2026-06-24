from flask import Flask, render_template, request, jsonify
import sqlite3
# Naya function import kiya
from AI import ai_menu_suggestor, train_and_predict_occupancy 

app = Flask(__name__)

# ---------------- पेजों को लोड करने के रूट्स (Frontend Routes) ----------------

# 1. कस्टमर के लिए होमपेज (index.html)
@app.route('/')
def home():
    return render_template('index.html')

# 2. ओनर के लिए सीक्रेट एडमिन पैनल (admin.html)
@app.route('/admin')
def admin_panel():
    return render_template('admin.html')


# ---------------- बैकएंड एपीआई रूट्स (Backend API Routes) ----------------

# 1. API: AI सर्च सजेशन
@app.route('/api/search', methods=['POST'])
def search_food():
    data = request.json or {}
    user_message = data.get('message', '')
    
    print(f"[TRACK LOG] User Searched: {user_message}") # बातचीत ट्रैक करना
    
    suggestions = ai_menu_suggestor(user_message)
    formatted_suggestions = [
        {"name": item[0], "price": item[1], "description": item[2]} for item in suggestions
    ]
    return jsonify({"status": "success", "data": formatted_suggestions})

# 2. API: स्लॉट बुकिंग
@app.route('/api/book', methods=['POST'])
def book_slot():
    data = request.json or {}
    name = data.get('name')
    seat = data.get('seat')
    date = data.get('date')
    time = data.get('time')
    
    conn = sqlite3.connect('cafe_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bookings (customer_name, seat_number, booking_date, booking_time) VALUES (?, ?, ?, ?)",
                   (name, seat, date, time))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Booking confirmed!"})

# 3. API: ML सीट Occupancy Percentage प्रेडिक्शन (Updated Route)
@app.route('/api/predict-seat', methods=['POST'])
def get_seat_prediction():
    data = request.json or {}
    target_date = data.get('date', '')
    
    if not target_date:
        return jsonify({"status": "error", "message": "Date is required"})
        
    # AI.py ke naye Percentage model function ko call karna
    prediction_result = train_and_predict_occupancy(target_date)
    
    return jsonify({"status": "success", "prediction": prediction_result})

# 4. API: ओनर डैशबोर्ड डेटा
@app.route('/api/admin/dashboard', methods=['GET'])
def admin_dashboard():
    conn = sqlite3.connect('cafe_database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        "bookings": bookings,
        "orders": orders
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)