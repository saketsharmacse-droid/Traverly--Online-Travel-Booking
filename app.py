from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
from fpdf import FPDF
import random
import string

app = Flask(__name__)
CORS(app)

# Enhanced database with more destinations and details
bookings_db = []

# Enhanced flights database with more destinations
flights_db = [
    # Domestic Flights
    {"id": "6E2342", "airline": "IndiGo", "from": "Delhi", "to": "Goa", "departure": "06:00", "arrival": "08:30", "price": 4599, "type": "Non-stop", "duration": "2h 30m", "aircraft": "Boeing 737", "rating": 4.2, "reviews": 1250},
    {"id": "AI801", "airline": "Air India", "from": "Mumbai", "to": "Kerala", "departure": "10:15", "arrival": "12:45", "price": 5299, "type": "Non-stop", "duration": "2h 30m", "aircraft": "Airbus A320", "rating": 4.0, "reviews": 890},
    {"id": "SG415", "airline": "SpiceJet", "from": "Bangalore", "to": "Jaipur", "departure": "14:30", "arrival": "17:00", "price": 3899, "type": "1 Stop", "duration": "4h 30m", "aircraft": "Boeing 737", "rating": 3.8, "reviews": 567},
    {"id": "UK881", "airline": "Vistara", "from": "Kolkata", "to": "Dubai", "departure": "23:00", "arrival": "03:30", "price": 18999, "type": "Non-stop", "duration": "6h 30m", "aircraft": "Boeing 787", "rating": 4.5, "reviews": 2340},
    {"id": "IX344", "airline": "Air India Express", "from": "Chennai", "to": "Singapore", "departure": "05:45", "arrival": "12:30", "price": 15999, "type": "Non-stop", "duration": "4h 45m", "aircraft": "Boeing 737", "rating": 4.1, "reviews": 1100},
    
    # Additional flights for enhanced destinations
    {"id": "6E789", "airline": "IndiGo", "from": "Hyderabad", "to": "Thailand", "departure": "02:30", "arrival": "08:45", "price": 22999, "type": "Non-stop", "duration": "4h 15m", "aircraft": "Airbus A321", "rating": 4.3, "reviews": 890},
    {"id": "SG234", "airline": "SpiceJet", "from": "Pune", "to": "Maldives", "departure": "11:20", "arrival": "15:30", "price": 35999, "type": "1 Stop", "duration": "6h 10m", "aircraft": "Boeing 737", "rating": 4.0, "reviews": 445},
    {"id": "AI567", "airline": "Air India", "from": "Ahmedabad", "to": "Bali", "departure": "16:45", "arrival": "02:30", "price": 28999, "type": "1 Stop", "duration": "8h 45m", "aircraft": "Boeing 787", "rating": 4.2, "reviews": 678},
    {"id": "6E456", "airline": "IndiGo", "from": "Delhi", "to": "Kashmir", "departure": "07:30", "arrival": "09:00", "price": 6899, "type": "Non-stop", "duration": "1h 30m", "aircraft": "Airbus A320", "rating": 4.4, "reviews": 1567},
    {"id": "UK123", "airline": "Vistara", "from": "Mumbai", "to": "Manali", "departure": "09:45", "arrival": "11:15", "price": 5499, "type": "Non-stop", "duration": "1h 30m", "aircraft": "Airbus A320", "rating": 4.3, "reviews": 890},
]

# Enhanced hotels database
hotels_db = [
    {"id": "HTL001", "name": "Ocean Pearl Resort", "location": "Goa", "rating": 5, "price": 8999, "amenities": ["Beach View", "WiFi", "Breakfast", "Pool", "Spa"], "reviews": 2340, "description": "Luxury beachfront resort with stunning ocean views"},
    {"id": "HTL002", "name": "Coral Beach Hotel", "location": "Goa", "rating": 4, "price": 5499, "amenities": ["Sea View", "AC", "Breakfast", "Bar", "Gym"], "reviews": 1567, "description": "Comfortable hotel with excellent amenities"},
    {"id": "HTL003", "name": "Mountain View Resort", "location": "Manali", "rating": 5, "price": 7999, "amenities": ["Mountain View", "Heating", "WiFi", "Restaurant"], "reviews": 1890, "description": "Spectacular mountain resort with panoramic views"},
    {"id": "HTL004", "name": "Backwater Paradise", "location": "Kerala", "rating": 5, "price": 9999, "amenities": ["Lake View", "Ayurveda Spa", "WiFi", "Restaurant"], "reviews": 1234, "description": "Serene backwater resort with traditional charm"},
    {"id": "HTL005", "name": "City Center Hotel", "location": "Mumbai", "rating": 4, "price": 6999, "amenities": ["City View", "WiFi", "Gym", "Restaurant", "Bar"], "reviews": 3456, "description": "Modern business hotel in heart of the city"},
    
    # Additional hotels for new destinations
    {"id": "HTL006", "name": "Kashmir Houseboat", "location": "Kashmir", "rating": 5, "price": 12999, "amenities": ["Lake View", "Traditional Decor", "Shikara Rides", "Local Cuisine"], "reviews": 567, "description": "Authentic Kashmir houseboat experience on Dal Lake"},
    {"id": "HTL007", "name": "Himalayan Retreat", "location": "Manali", "rating": 4, "price": 8999, "amenities": ["Mountain View", "Adventure Activities", "Bonfire", "Trekking"], "reviews": 890, "description": "Adventure resort in the heart of Himalayas"},
    {"id": "HTL008", "name": "Heritage Palace Hotel", "location": "Udaipur", "rating": 5, "price": 15999, "amenities": ["Palace View", "Royal Dining", "Spa", "Cultural Shows"], "reviews": 1890, "description": "Royal palace converted to luxury hotel"},
    {"id": "HTL009", "name": "Wellness Ashram", "location": "Rishikesh", "rating": 4, "price": 4999, "amenities": ["Yoga Classes", "Meditation", "Ayurveda", "Organic Food"], "reviews": 1123, "description": "Spiritual retreat center for wellness and peace"},
    {"id": "HTL010", "name": "Colonial Charm Hotel", "location": "Shimla", "rating": 4, "price": 7499, "amenities": ["Hill View", "Heritage Architecture", "Garden", "Library"], "reviews": 789, "description": "British colonial era hotel with old-world charm"},
]

# Enhanced trains database
trains_db = [
    {"id": "12002", "name": "Shatabdi Express", "from": "New Delhi", "to": "Agra", "departure": "06:00", "arrival": "14:00", "class": "AC Chair", "price": 1855, "duration": "8h 0m", "rating": 4.6, "reviews": 3450},
    {"id": "12301", "name": "Rajdhani Express", "from": "Mumbai Central", "to": "Jaipur", "departure": "16:30", "arrival": "10:30", "class": "AC 2 Tier", "price": 2455, "duration": "18h 0m", "rating": 4.3, "reviews": 2890},
    {"id": "12269", "name": "Duronto Express", "from": "Chennai Central", "to": "Varanasi", "departure": "23:00", "arrival": "17:00", "class": "AC 3 Tier", "price": 1355, "duration": "18h 0m", "rating": 4.2, "reviews": 1234},
    {"id": "12650", "name": "Karnataka Express", "from": "Bangalore City", "to": "Kochi", "departure": "19:20", "arrival": "07:30", "class": "Sleeper", "price": 755, "duration": "12h 10m", "rating": 3.9, "reviews": 890},
    {"id": "12555", "name": "Gorakhdham Express", "from": "Howrah", "to": "Amritsar", "departure": "13:10", "arrival": "22:45", "class": "AC 3 Tier", "price": 1955, "duration": "33h 35m", "rating": 4.1, "reviews": 1567},
    
    # Additional trains
    {"id": "12345", "name": "Kashmir Express", "from": "New Delhi", "to": "Jammu", "departure": "20:30", "arrival": "06:30", "class": "AC 2 Tier", "price": 2155, "duration": "10h 0m", "rating": 4.4, "reviews": 1890},
    {"id": "12678", "name": "Himalayan Queen", "from": "New Delhi", "to": "Haridwar", "departure": "07:40", "arrival": "13:25", "class": "AC Chair", "price": 1255, "duration": "5h 45m", "rating": 4.2, "reviews": 1123},
    {"id": "12890", "name": "Konkan Express", "from": "Mumbai Central", "to": "Goa", "departure": "11:40", "arrival": "23:45", "class": "AC 3 Tier", "price": 1555, "duration": "12h 5m", "rating": 4.0, "reviews": 2345},
]

# Enhanced packages database
packages_db = [
    {
        "id": "PKG001", 
        "name": "Goa Beach Paradise", 
        "duration": "5D/4N", 
        "price": 25999, 
        "original_price": 32999,
        "discount": 22,
        "includes": ["Round-trip flights", "4-star beachfront resort", "Daily breakfast & dinner", "Water sports", "Airport transfers"],
        "highlights": ["Baga Beach", "Old Goa Churches", "Dudhsagar Falls"],
        "best_time": "Nov-Feb",
        "rating": 4.8,
        "reviews": 2340
    },
    {
        "id": "PKG002", 
        "name": "Himalayan Adventure", 
        "duration": "7D/6N", 
        "price": 35999, 
        "original_price": 45999,
        "discount": 20,
        "includes": ["Professional trek guide", "Mountain lodge accommodation", "All meals during trek", "Camping equipment", "Medical support"],
        "highlights": ["Rohtang Pass", "Solang Valley", "Manali Mall Road"],
        "best_time": "Mar-Jun, Sep-Nov",
        "rating": 4.7,
        "reviews": 1567
    },
    {
        "id": "PKG003", 
        "name": "Kerala Backwaters", 
        "duration": "4D/3N", 
        "price": 18999, 
        "original_price": 24999,
        "discount": 24,
        "includes": ["Private houseboat", "Ayurvedic spa treatments", "Traditional Kerala cuisine", "Backwater cruises", "Cultural performances"],
        "highlights": ["Alleppey Backwaters", "Munnar Hill Station", "Kochi Fort"],
        "best_time": "Sep-Mar",
        "rating": 4.6,
        "reviews": 1890
    },
    {
        "id": "PKG004", 
        "name": "Rajasthan Heritage", 
        "duration": "6D/5N", 
        "price": 42999, 
        "original_price": 54999,
        "discount": 22,
        "includes": ["Heritage palace hotels", "Guided fort & palace tours", "Camel safari", "Traditional cuisine", "Folk performances"],
        "highlights": ["Jaipur City Palace", "Udaipur Lakes", "Jaisalmer Fort"],
        "best_time": "Oct-Mar",
        "rating": 4.9,
        "reviews": 3456
    },
    {
        "id": "PKG005", 
        "name": "Andaman Islands", 
        "duration": "5D/4N", 
        "price": 32999, 
        "original_price": 42999,
        "discount": 23,
        "includes": ["Island hopping", "Scuba diving & snorkeling", "Beach resort", "Seafood specialties", "Water sports"],
        "highlights": ["Radhanagar Beach", "Cellular Jail", "Ross Island"],
        "best_time": "Oct-May",
        "rating": 4.5,
        "reviews": 1234
    },
    {
        "id": "PKG006", 
        "name": "Kashmir Paradise", 
        "duration": "5D/4N", 
        "price": 28999, 
        "original_price": 38999,
        "discount": 25,
        "includes": ["Houseboat stay in Dal Lake", "Shikara rides", "Gulmarg & Pahalgam visits", "Traditional cuisine", "Handicraft tours"],
        "highlights": ["Dal Lake", "Gulmarg Gondola", "Pahalgam Valley"],
        "best_time": "Apr-Oct",
        "rating": 4.8,
        "reviews": 890
    }
]

# Weather data for destinations
weather_data = {
    "goa": {"temp": "28°C", "condition": "Perfect beach weather", "icon": "🌤️"},
    "kerala": {"temp": "26°C", "condition": "Pleasant monsoon season", "icon": "🌧️"},
    "rajasthan": {"temp": "32°C", "condition": "Warm desert climate", "icon": "☀️"},
    "kashmir": {"temp": "18°C", "condition": "Cool mountain weather", "icon": "❄️"},
    "manali": {"temp": "15°C", "condition": "Crisp mountain air", "icon": "🏔️"},
    "andaman": {"temp": "30°C", "condition": "Tropical paradise", "icon": "🏝️"}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search/flights', methods=['POST'])
def search_flights():
    data = request.json
    from_city = data.get('from', '').lower()
    to_city = data.get('to', '').lower()
    date = data.get('date')
    passengers = data.get('passengers', 1)
    
    # Enhanced filtering logic
    results = []
    for flight in flights_db:
        if (from_city in flight['from'].lower() or 
            to_city in flight['to'].lower() or
            from_city == '' or to_city == ''):
            
            # Add dynamic pricing based on demand
            base_price = flight['price']
            demand_multiplier = random.uniform(0.85, 1.25)
            flight_copy = flight.copy()
            flight_copy['price'] = int(base_price * demand_multiplier)
            flight_copy['original_price'] = base_price
            flight_copy['discount'] = max(0, int((1 - demand_multiplier) * 100))
            
            results.append(flight_copy)
    
    # Sort by price if no specific matches found
    if not results:
        results = sorted(flights_db[:3], key=lambda x: x['price'])
    
    # Limit results and sort by rating
    results = sorted(results[:5], key=lambda x: x.get('rating', 0), reverse=True)
    
    return jsonify(results)

@app.route('/api/search/hotels', methods=['POST'])
def search_hotels():
    data = request.json
    destination = data.get('destination', '').lower()
    checkin = data.get('checkin')
    checkout = data.get('checkout')
    guests = data.get('guests', 2)
    
    # Enhanced filtering
    results = []
    for hotel in hotels_db:
        if destination in hotel['location'].lower() or destination == '':
            # Dynamic pricing based on occupancy simulation
            base_price = hotel['price']
            occupancy_multiplier = random.uniform(0.8, 1.4)
            hotel_copy = hotel.copy()
            hotel_copy['price'] = int(base_price * occupancy_multiplier)
            hotel_copy['original_price'] = base_price
            hotel_copy['discount'] = max(0, int((1 - occupancy_multiplier) * 100))
            
            # Add availability status
            hotel_copy['availability'] = random.choice(['Available', 'Only 2 rooms left', 'High demand'])
            
            results.append(hotel_copy)
    
    if not results:
        results = sorted(hotels_db[:3], key=lambda x: x['rating'], reverse=True)
    
    # Sort by rating
    results = sorted(results[:5], key=lambda x: x.get('rating', 0), reverse=True)
    
    return jsonify(results)

@app.route('/api/search/trains', methods=['POST'])
def search_trains():
    data = request.json
    from_station = data.get('from', '').lower()
    to_station = data.get('to', '').lower()
    date = data.get('date')
    travel_class = data.get('class', '')
    
    # Enhanced filtering
    results = []
    for train in trains_db:
        if (from_station in train['from'].lower() or 
            to_station in train['to'].lower() or
            from_station == '' or to_station == ''):
            
            train_copy = train.copy()
            # Add seat availability
            train_copy['seats_available'] = random.randint(5, 50)
            train_copy['waiting_list'] = random.randint(0, 20)
            
            results.append(train_copy)
    
    if not results:
        results = trains_db[:3]
    
    # Sort by departure time
    results = sorted(results[:5], key=lambda x: x.get('rating', 0), reverse=True)
    
    return jsonify(results)

@app.route('/api/packages', methods=['GET'])
def get_packages():
    # Add real-time pricing updates
    updated_packages = []
    for package in packages_db:
        package_copy = package.copy()
        # Simulate seasonal pricing
        seasonal_multiplier = random.uniform(0.9, 1.1)
        package_copy['current_price'] = int(package['price'] * seasonal_multiplier)
        updated_packages.append(package_copy)
    
    return jsonify(updated_packages)

@app.route('/api/weather/<destination>', methods=['GET'])
def get_weather(destination):
    weather = weather_data.get(destination.lower(), {
        "temp": "25°C", 
        "condition": "Pleasant weather", 
        "icon": "🌤️"
    })
    return jsonify(weather)

@app.route('/api/book', methods=['POST'])
def book_service():
    data = request.json
    booking_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    # Enhanced booking with more details
    booking = {
        'id': booking_id,
        'type': data.get('type'),
        'service_id': data.get('service_id'),
        'service_name': data.get('service_name'),
        'price': data.get('price'),
        'user_details': data.get('user_details', {}),
        'booking_date': datetime.now().strftime('%Y-%m-%d'),
        'booking_time': datetime.now().strftime('%H:%M:%S'),
        'status': 'confirmed',
        'payment_method': data.get('payment_method', 'Credit Card'),
        'extras': data.get('extras', {}),
        'special_requests': data.get('special_requests', ''),
        'contact_info': {
            'email': 'customer@example.com',
            'phone': '+91-9876543210'
        }
    }
    
    bookings_db.append(booking)
    
    # Enhanced pricing calculation
    subtotal = booking['price']
    convenience_fee = int(subtotal * 0.02)  # 2% convenience fee
    gst = int((subtotal + convenience_fee) * 0.18)  # 18% GST
    total = subtotal + convenience_fee + gst
    
    # Simulate payment processing
    payment_status = random.choice(['success', 'success', 'success', 'pending'])  # 75% success rate
    
    response = {
        'booking_id': booking_id,
        'subtotal': subtotal,
        'convenience_fee': convenience_fee,
        'gst': gst,
        'total': total,
        'status': 'confirmed' if payment_status == 'success' else 'pending',
        'payment_status': payment_status,
        'estimated_processing_time': '2-4 hours',
        'cancellation_policy': 'Free cancellation up to 24 hours before travel'
    }
    
    return jsonify(response)

@app.route('/api/generate-bill/<booking_id>', methods=['GET'])
def generate_bill(booking_id):
    # Find booking
    booking = next((b for b in bookings_db if b['id'] == booking_id), None)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    # Enhanced PDF generation
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font('Arial', 'B', 28)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 20, 'TRAVERLY', 0, 1, 'C')
    
    pdf.set_font('Arial', '', 14)
    pdf.set_text_color(102, 102, 102)
    pdf.cell(0, 10, 'Your Ocean of Adventures', 0, 1, 'C')
    pdf.cell(0, 5, 'Creating magical travel moments since 2024', 0, 1, 'C')
    pdf.ln(10)
    
    # Invoice header
    pdf.set_font('Arial', 'B', 18)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 15, 'BOOKING INVOICE', 0, 1, 'C')
    pdf.ln(5)
    
    # Booking details
    pdf.set_font('Arial', '', 12)
    details = [
        f'Booking ID: {booking["id"]}',
        f'Date: {booking["booking_date"]} at {booking["booking_time"]}',
        f'Type: {booking["type"]}',
        f'Service: {booking["service_name"]}',
        f'Status: {booking["status"].upper()}',
        f'Payment Method: {booking.get("payment_method", "Credit Card")}'
    ]
    
    for detail in details:
        pdf.cell(0, 8, detail, 0, 1)
    
    pdf.ln(5)
    
    # Price breakdown
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 12, 'PRICE BREAKDOWN', 0, 1)
    pdf.set_font('Arial', '', 11)
    
    subtotal = booking['price']
    convenience_fee = int(subtotal * 0.02)
    gst = int((subtotal + convenience_fee) * 0.18)
    total = subtotal + convenience_fee + gst
    
    price_items = [
        ('Base Amount:', f'Rs. {subtotal:,}'),
        ('Convenience Fee (2%):', f'Rs. {convenience_fee:,}'),
        ('GST (18%):', f'Rs. {gst:,}')
    ]
    
    for item, amount in price_items:
        pdf.cell(100, 8, item, 0, 0)
        pdf.cell(0, 8, amount, 0, 1, 'R')
    
    # Total
    pdf.set_font('Arial', 'B', 14)
    pdf.ln(5)
    pdf.cell(100, 12, 'TOTAL AMOUNT:', 1, 0, '', True)
    pdf.cell(0, 12, f'Rs. {total:,}', 1, 1, 'R', True)
    
    # Footer
    pdf.ln(15)
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(102, 102, 102)
    
    footer_lines = [
        'Thank you for choosing Traverly!',
        '',
        'Customer Support: support@traverly.com | +91-1800-TRAVERLY',
        'Website: www.traverly.com',
        '',
        'Terms & Conditions apply. Please read our cancellation policy.',
        'Safe travels and create beautiful memories!',
        '',
        'Made with love by Saket'
    ]
    
    for line in footer_lines:
        pdf.cell(0, 6, line, 0, 1, 'C')
    
    # Save PDF
    filename = f'bill_{booking_id}.pdf'
    pdf.output(filename)
    
    return send_file(filename, as_attachment=True, download_name=f'Traverly_Invoice_{booking_id}.pdf')

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    # Return bookings with enhanced information
    enhanced_bookings = []
    for booking in bookings_db:
        enhanced_booking = booking.copy()
        # Add calculated totals
        subtotal = booking['price']
        convenience_fee = int(subtotal * 0.02)
        gst = int((subtotal + convenience_fee) * 0.18)
        enhanced_booking['total_amount'] = subtotal + convenience_fee + gst
        enhanced_bookings.append(enhanced_booking)
    
    return jsonify(enhanced_bookings)

@app.route('/api/destinations', methods=['GET'])
def get_destinations():
    """Get popular destinations with details"""
    destinations = [
        {
            "name": "Goa",
            "type": "Beach",
            "rating": 4.8,
            "image": "beach.jpg",
            "best_time": "Nov-Feb",
            "highlights": ["Baga Beach", "Old Goa", "Dudhsagar Falls"],
            "starting_price": 15999
        },
        {
            "name": "Kashmir",
            "type": "Mountains",
            "rating": 4.9,
            "image": "mountains.jpg",
            "best_time": "Apr-Oct",
            "highlights": ["Dal Lake", "Gulmarg", "Pahalgam"],
            "starting_price": 22999
        },
        {
            "name": "Kerala",
            "type": "Backwaters",
            "rating": 4.7,
            "image": "backwaters.jpg",
            "best_time": "Sep-Mar",
            "highlights": ["Alleppey", "Munnar", "Kochi"],
            "starting_price": 18999
        }
    ]
    return jsonify(destinations)

@app.route('/api/reviews/<service_type>/<service_id>', methods=['GET'])
def get_reviews(service_type, service_id):
    """Get reviews for a specific service"""
    # Simulated reviews - in production, this would come from a database
    sample_reviews = [
        {
            "user": "Rahul S.",
            "rating": 5,
            "comment": "Excellent service! Highly recommended.",
            "date": "2024-01-15",
            "verified": True
        },
        {
            "user": "Priya M.",
            "rating": 4,
            "comment": "Good experience overall. Will book again.",
            "date": "2024-01-10",
            "verified": True
        }
    ]
    return jsonify(sample_reviews)

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create templates folder if not exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create static folder for images
    if not os.path.exists('static'):
        os.makedirs('static')
    
    print("🌊 Starting Traverly - Your Ocean of Adventures!")
    print("📡 Server running on http://localhost:5000")
    print("❤️ Made with love by Saket")
    
    app.run(debug=True, port=5000, host='0.0.0.0')