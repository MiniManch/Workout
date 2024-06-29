from flask import Blueprint, request, jsonify
from data.setup_db import get_db_connection

client_bp = Blueprint('client', __name__, url_prefix='/client')

@client_bp.route('/get_coach_client_data/<int:coach_id>', methods=['GET'])
def get_clients_by_coach(coach_id):
    try:
        db = get_db_connection()
        query = "SELECT ClientID, Name, Email, PhoneNumber FROM client WHERE CoachID = %s"
        cursor = db.cursor()
        cursor.execute(query, (coach_id,))
        clients = cursor.fetchall()

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
        db = get_db_connection()
        data = request.get_json()
        new_name = data.get('name')
        new_email = data.get('email')
        new_phone = data.get('phone')

        update_query = "UPDATE client SET Name = %s, Email = %s, PhoneNumber = %s WHERE ClientID = %s"
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
        db = get_db_connection()
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')

        insert_query = "INSERT INTO client (Name, Email, PhoneNumber, CoachID) VALUES (%s, %s, %s, %s)"
        cursor = db.cursor()
        cursor.execute(insert_query, (name, email, phone, coach_id))
        db.commit()

        new_client_id = cursor.lastrowid

        return jsonify({'message': 'Client added successfully', 'client_id': new_client_id}), 201

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        db.close()

@client_bp.route('/delete/<int:coach_id>/<int:client_id>', methods=['DELETE'])
def delete_client(coach_id, client_id):
    try:
        db = get_db_connection()

        # Check if the client belongs to the coach
        check_query = "SELECT CoachID FROM client WHERE ClientID = %s"
        cursor = db.cursor()
        print(f"Executing query: {check_query} with client_id={client_id}")  # Debug print
        cursor.execute(check_query, (client_id,))
        result = cursor.fetchone()

        if result is None:
            return jsonify({'error': 'Client not found'}), 404

        client_coach_id = result[0]
        if client_coach_id != coach_id:
            return jsonify({'error': 'Unauthorized to delete this client'}), 403

        # Delete the client if it belongs to the coach
        delete_query = "DELETE FROM client WHERE ClientID = %s"
        print(f"Executing delete query: {delete_query} with client_id={client_id}")  # Debug print
        cursor.execute(delete_query, (client_id,))
        db.commit()

        return jsonify({'message': 'Client deleted successfully'}), 200

    except Exception as e:
        db.rollback()
        print(f"Error occurred: {str(e)}")  # Detailed error logging
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        db.close()

@client_bp.route('/get_client/<int:client_id>', methods=['GET'])
def get_client_by_id(client_id):
    print(client_id)
    try:
        db = get_db_connection()
        query = "SELECT ClientID, Name, Email, PhoneNumber, CoachID FROM Client WHERE ClientID = %s"
        cursor = db.cursor()
        cursor.execute(query, (client_id,))
        client = cursor.fetchone()

        if client is None:
            return jsonify({'error': 'Client not found'}), 404

        client_data = {
            'id': client[0],
            'name': client[1],
            'email': client[2],
            'phone': client[3],
            'coach_id': client[4]
        }

        return jsonify({'client': client_data}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        db.close()