from flask import Blueprint, request, jsonify
from data.setup_db import get_db_connection

coach_bp = Blueprint('coach', __name__, url_prefix='/coach')

@coach_bp.route('/create', methods=['POST'])
def create_coach():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')

    if not name or not email or not phone:
        return jsonify({'message': 'Name, email, and phone are required'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Check for existing coach with the same name or email
        check_query = "SELECT * FROM Coach WHERE Name = %s OR Email = %s"
        cursor.execute(check_query, (name, email))
        existing_coach = cursor.fetchone()

        if existing_coach:
            return jsonify({'message': 'A coach with the same name or email already exists'}), 409

        # Insert the new coach if no duplicates are found
        insert_query = "INSERT INTO Coach (Name, Email, PhoneNumber) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (name, email, phone))
        connection.commit()

        return jsonify({'message': 'Coach created successfully'}), 201
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@coach_bp.route('/login', methods=['POST'])
def login_coach():
    data = request.json
    coach_name = data.get('name')
    
    if not coach_name:
        return jsonify({'message': 'Coach name is required'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = "SELECT * FROM Coach WHERE Name = %s"
        cursor.execute(query, (coach_name,))
        result = cursor.fetchone()

        if result:
            coach_data = {
                'id': result[0],
                'name': result[1],
                'email': result[2],
                'phone': result[3]
            }
            return jsonify({'message': 'Coach logged in successfully', 'coach_data': coach_data}), 200
        else:
            return jsonify({'message': 'Coach not found'}), 404
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@coach_bp.route('/<field>', methods=['PUT'])
def update_field(field):
    data = request.json
    value = data.get('value')
    coach_id = request.headers.get('CoachID')

    if field not in ['name', 'email', 'phone']:
        return jsonify({'message': 'Invalid field'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        if field == 'email':
            # Check for duplicate email (case-insensitive)
            cursor.execute("SELECT * FROM Coach WHERE LOWER(Email) = LOWER(%s) AND CoachID != %s", (value, coach_id))
            if cursor.fetchone():
                return jsonify({'message': 'Email already exists'}), 400
        
        if field == 'name':
            # Check for duplicate name (case-insensitive)
            cursor.execute("SELECT * FROM Coach WHERE LOWER(Name) = LOWER(%s) AND CoachID != %s", (value, coach_id))
            if cursor.fetchone():
                return jsonify({'message': 'Name already exists'}), 400
        
        if field == 'phone':
            # Check for duplicate phone number (exact match)
            cursor.execute("SELECT * FROM Coach WHERE PhoneNumber = %s AND CoachID != %s", (value, coach_id))
            if cursor.fetchone():
                return jsonify({'message': 'Phone number already exists'}), 400

        # Create dynamic SQL query based on the field
        field_name = 'PhoneNumber' if field == 'phone' else field.capitalize()
        query = f"UPDATE Coach SET {field_name} = %s WHERE CoachID = %s"
        cursor.execute(query, (value, coach_id))
        connection.commit()
        return jsonify({'message': f'{field.capitalize()} updated successfully'}), 200
    except Exception as e:
        connection.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()