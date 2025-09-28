from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import json
import os
from fpdf import FPDF
import random
import string

app = Flask(__name__)
CORS(app)

# Simple database (in production, use a real database)
bookings_db = []
flights_db = [
    {"id": "6E2342", "airline": "IndiGo", "from": "Delhi", "to": "Goa", "departure": "06:00", "arrival": "08:30", "price": 4599, "type": "Non-stop"},
    {"id": "AI801", "airline": "Air India", "from": "Mumbai", "to": "Kerala", "departure": "10:15", "arrival": "12:45", "price": 5299, "type": "Non-stop"},
    {"id": "SG415", "airline": "SpiceJet", "from": "Bangalore", "to": "Jaipur", "departure": "14:30", "arrival": "17:00", "price": 3899, "type": "1 Stop"},
    {"id": "UK881", "airline": "Vistara", "from": "Kolkata", "to": "Dubai", "departure": "23:00", "arrival": "03:30", "price": 18999, "type": "Non-stop"},
    {"id": "IX344", "airline": "Air India Express", "from": "Chennai", "to": "Singapore", "departure": "05:45", "arrival": "12:30", "price": 15999, "type": "Non-stop"},
]

hotels_db = [
    {"id": "HTL001", "name": "Ocean Pearl Resort", "location": "Goa", "rating": 5, "price": 8999, "amenities": ["Beach View", "WiFi", "Breakfast", "Pool", "Spa"]},
    {"id": "HTL002", "name": "Coral Beach Hotel", "location": "Goa", "rating": 4, "price": 5499, "amenities": ["Sea View", "AC", "Breakfast", "Bar", "Gym"]},
    {"id": "HTL003", "name": "Mountain View Resort", "location": "Manali", "rating": 5, "price": 7999, "amenities": ["Mountain View", "Heating", "WiFi", "Restaurant"]},
    {"id": "HTL004", "name": "Backwater Paradise", "location": "Kerala", "rating": 5, "price": 9999, "amenities": ["Lake View", "Ayurveda Spa", "WiFi", "Restaurant"]},
    {"id": "HTL005", "name": "City Center Hotel", "location": "Mumbai", "rating": 4, "price": 6999, "amenities": ["City View", "WiFi", "Gym", "Restaurant", "Bar"]},
]

trains_db = [
    {"id": "12002", "name": "Shatabdi Express", "from": "New Delhi", "to": "Agra", "departure": "06:00", "arrival": "14:00", "class": "AC Chair", "price": 1855},
    {"id": "12301", "name": "Rajdhani Express", "from": "Mumbai Central", "to": "Jaipur", "departure": "16:30", "arrival": "10:30", "class": "AC 2 Tier", "price": 2455},
    {"id": "12269", "name": "Duronto Express", "from": "Chennai Central", "to": "Varanasi", "departure": "23:00", "arrival": "17:00", "class": "AC 3 Tier", "price": 1355},
    {"id": "12650", "name": "Karnataka Express", "from": "Bangalore City", "to": "Kochi", "departure": "19:20", "arrival": "07:30", "class": "Sleeper", "price": 755},
    {"id": "12555", "name": "Gorakhdham Express", "from": "Howrah", "to": "Amritsar", "departure": "13:10", "arrival": "22:45", "class": "AC 3 Tier", "price": 1955},
]

packages_db = [
    {"id": "PKG001", "name": "Goa Beach Paradise", "duration": "5D/4N", "price": 25999, "includes": ["Flight", "Hotel", "Meals", "Sightseeing"]},
    {"id": "PKG002", "name": "Himalayan Adventure", "duration": "7D/6N", "price": 35999, "includes": ["Transport", "Hotel", "Meals", "Trekking", "Guide"]},
    {"id": "PKG003", "name": "Kerala Backwaters", "duration": "4D/3N", "price": 18999, "includes": ["Transport", "Houseboat", "Resort", "Ayurveda", "Meals"]},
    {"id": "PKG004", "name": "Rajasthan Heritage", "duration": "6D/5N", "price": 42999, "includes": ["Flight", "Palace Hotels", "Cultural Tours", "Meals"]},
    {"id": "PKG005", "name": "Andaman Islands", "duration": "5D/4N", "price": 32999, "includes": ["Flight", "Hotel", "Island Hopping", "Water Sports", "Meals"]},
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search/flights', methods=['POST'])
def search_flights():
    data = request.json
    from_city = data.get('from')
    to_city = data.get('to')
    date = data.get('date')
    
    # Filter flights based on criteria
    results = []
    for flight in flights_db:
        if flight['from'].lower() == from_city.lower() or flight['to'].lower() == to_city.lower():
            results.append(flight)
    
    # If no exact matches, return all flights
    if not results:
        results = flights_db[:3]
    
    return jsonify(results)

@app.route('/api/search/hotels', methods=['POST'])
def search_hotels():
    data = request.json
    destination = data.get('destination')
    checkin = data.get('checkin')
    checkout = data.get('checkout')
    
    # Filter hotels based on destination
    results = []
    for hotel in hotels_db:
        if destination and hotel['location'].lower() == destination.lower():
            results.append(hotel)
    
    # If no exact matches, return top hotels
    if not results:
        results = hotels_db[:3]
    
    return jsonify(results)

@app.route('/api/search/trains', methods=['POST'])
def search_trains():
    data = request.json
    from_station = data.get('from')
    to_station = data.get('to')
    date = data.get('date')
    
    # Filter trains
    results = []
    for train in trains_db:
        if train['from'].lower() == from_station.lower() or train['to'].lower() == to_station.lower():
            results.append(train)
    
    if not results:
        results = trains_db[:3]
    
    return jsonify(results)

@app.route('/api/packages', methods=['GET'])
def get_packages():
    return jsonify(packages_db)

@app.route('/api/book', methods=['POST'])
def book_service():
    data = request.json
    booking_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    booking = {
        'id': booking_id,
        'type': data.get('type'),
        'service_id': data.get('service_id'),
        'service_name': data.get('service_name'),
        'price': data.get('price'),
        'user_details': data.get('user_details', {}),
        'booking_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'confirmed'
    }
    
    bookings_db.append(booking)
    
    # Calculate total with GST
    subtotal = booking['price']
    gst = int(subtotal * 0.18)
    total = subtotal + gst
    
    return jsonify({
        'booking_id': booking_id,
        'subtotal': subtotal,
        'gst': gst,
        'total': total,
        'status': 'confirmed'
    })

@app.route('/api/generate-bill/<booking_id>', methods=['GET'])
def generate_bill(booking_id):
    # Find booking
    booking = next((b for b in bookings_db if b['id'] == booking_id), None)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 15, 'TRAVERLY', 0, 1, 'C')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'Your Ocean of Adventures', 0, 1, 'C')
    pdf.ln(10)
    
    # Add booking details
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'BOOKING INVOICE', 0, 1, 'C')
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 8, f'Booking ID: {booking["id"]}', 0, 1)
    pdf.cell(0, 8, f'Date: {booking["booking_date"]}', 0, 1)
    pdf.cell(0, 8, f'Type: {booking["type"]}', 0, 1)
    pdf.cell(0, 8, f'Service: {booking["service_name"]}', 0, 1)
    pdf.ln(5)
    
    # Price details
    subtotal = booking['price']
    gst = int(subtotal * 0.18)
    total = subtotal + gst
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'PRICE DETAILS', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(100, 8, 'Base Amount:', 0, 0)
    pdf.cell(0, 8, f'Rs. {subtotal:,}', 0, 1, 'R')
    pdf.cell(100, 8, 'GST (18%):', 0, 0)
    pdf.cell(0, 8, f'Rs. {gst:,}', 0, 1, 'R')
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(100, 10, 'Total Amount:', 0, 0)
    pdf.cell(0, 10, f'Rs. {total:,}', 0, 1, 'R')
    
    pdf.ln(20)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 8, 'Thank you for choosing Traverly!', 0, 1, 'C')
    pdf.cell(0, 8, 'Contact: support@traverly.com | +91-1800-TRAVERLY', 0, 1, 'C')
    
    # Save PDF
    filename = f'bill_{booking_id}.pdf'
    pdf.output(filename)
    
    return send_file(filename, as_attachment=True, download_name=f'Traverly_Invoice_{booking_id}.pdf')

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    return jsonify(bookings_db)

if __name__ == '__main__':
    # Create templates folder if not exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Save the HTML to templates/index.html
    # In production, you would have the HTML file already created
    app.run(debug=True, port=5000)