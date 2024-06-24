from flask import Blueprint, request, jsonify
from data.setup_db import get_db_connection 
client_bp = Blueprint('client', __name__, url_prefix='/client')

@client_bp.route('/<int:coach_id>/clients', methods=['GET'])
def get_clients_by_coach(coach_id):
    try:
        # Get database connection
        db = get_db_connection()
        # Query clients for the specified coach_id
        query = "SELECT ClientID, Name, Email, PhoneNumber FROM client WHERE CoachID = %s"
        cursor = db.cursor()
        cursor.execute(query, (coach_id,))
        clients = cursor.fetchall()

        # Convert result to list of dictionaries
        clients_list = []
        for client in clients:
            client_dict = {
                'id': client[0],
                'name': client[1],
                'email': client[2],
                'phone': client[3]
            }
            clients_list.append(client_dict)

        return jsonify({'clients': clients_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        db.close()

@client_bp.route('/update/<int:client_id>', methods=['POST'])
def update_client(client_id):
    try:
        # Get database connection
        db = get_db_connection()

        # Fetch client data from request body
        data = request.get_json()
        new_name = data.get('name')
        new_email = data.get('email')
        new_phone = data.get('phone')

        # Update client's information in the database
        update_query = "UPDATE client SET name = %s, email = %s, phone = %s WHERE id = %s"
        cursor = db.cursor()
        cursor.execute(update_query, (new_name, new_email, new_phone, client_id))
        db.commit()

        return jsonify({'message': 'Client updated successfully'}), 200

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        db.close()

@client_bp.route('/add/<int:coach_id>', methods=['POST'])
def add_client(coach_id):
    try:
        # Get database connection
        db = get_db_connection()

        # Fetch client data from request body
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')

        # Insert new client into the database
        insert_query = "INSERT INTO client (Name, Email, PhoneNumber, CoachID) VALUES (%s, %s, %s, %s)"
        cursor = db.cursor()
        cursor.execute(insert_query, (name, email, phone, coach_id))
        db.commit()

        # Get the newly inserted client ID
        new_client_id = cursor.lastrowid

        return jsonify({'message': 'Client added successfully', 'client_id': new_client_id}), 201

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()