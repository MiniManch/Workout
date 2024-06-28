from flask import Blueprint, jsonify, request
import json
from data.setup_db import get_db_connection
import pymysql
from datetime import timedelta

session_bp = Blueprint('session', __name__, url_prefix='/session')

@session_bp.route('/get_coach_sessions/<int:coach_id>', methods=['GET'])
def get_sessions_by_coach(coach_id):
    try:
        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
        # Query to fetch sessions with associated client details
        query = """
            SELECT s.SessionID, s.SessionName, s.Date, s.StartTime, s.Duration, c.ClientID, c.Name AS ClientName
            FROM Session AS s
            JOIN SessionClient AS sc ON s.SessionID = sc.SessionID
            JOIN Client AS c ON sc.ClientID = c.ClientID
            WHERE s.CoachID = %s
        """
        
        cursor.execute(query, (coach_id,))
        sessions = cursor.fetchall()
        
        cursor.close()
        db.close()

        if sessions:
            # Convert timedelta to string in the result
            for session in sessions:
                session['Duration'] = str(session['Duration'])

            return json.dumps({'sessions': sessions}, indent=4, sort_keys=True, default=str), 200
        else:
            return json.dumps({'message': 'No sessions found for this coach'}, indent=4, sort_keys=True, default=str), 404
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Detailed error logging
        return json.dumps({'error': str(e)}, indent=4, sort_keys=True, default=str), 500


@session_bp.route('/update/<int:session_id>', methods=['POST'])
def update_session(session_id):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        data = request.get_json()
        new_name = data.get('name')
        new_date = data.get('date')
        new_time = data.get('time')

        update_query = "UPDATE Session SET SessionName = %s, Date = %s, Time = %s WHERE SessionID = %s"
        cursor.execute(update_query, (new_name, new_date, new_time, session_id))
        db.commit()
        return json.dumps({'message': 'Session updated successfully'}, indent=4, sort_keys=True, default=str), 200

    except Exception as e:
        db.rollback()
        return json.dumps({'error': str(e)}, indent=4, sort_keys=True, default=str), 500

    finally:
        cursor.close()
        db.close()

@session_bp.route('/add/<int:coach_id>', methods=['POST'])
def add_session(coach_id):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        data = request.get_json()
        name = data.get('name')
        date = data.get('date')
        time = data.get('time')
        duration = data.get('duration')
        client_id = data.get('client_id')

        # Insert into Session table
        insert_session_query = "INSERT INTO Session (SessionName, Date, StartTime, CoachID,Duration) VALUES (%s, %s, %s, %s,%s)"
        cursor.execute(insert_session_query, (name, date, time, coach_id,duration))
        db.commit()
        session_id = cursor.lastrowid

        # Insert into SessionClient table to associate clients with session
        insert_session_client_query = "INSERT INTO SessionClient (SessionID, ClientID) VALUES (%s, %s)"
        cursor.execute(insert_session_client_query, (session_id, client_id))
        db.commit()

        return json.dumps({'message': 'Session added successfully', 'session_id': session_id}, indent=4, sort_keys=True, default=str), 201

    except Exception as e:
        db.rollback()
        print(str(e))
        return json.dumps({'error': str(e)}, indent=4, sort_keys=True, default=str), 500

    finally:
        cursor.close()
        db.close()


@session_bp.route('/delete/<int:coach_id>/<int:session_id>', methods=['DELETE'])
def delete_session(coach_id, session_id):
    try:
        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # Check if the session belongs to the coach
        check_query = "SELECT CoachID FROM Session WHERE SessionID = %s"
        cursor.execute(check_query, (session_id,))
        result = cursor.fetchone()

        if result is None:
            return json.dumps({'error': 'Session not found'}, indent=4, sort_keys=True, default=str), 404

        session_coach_id = result['CoachID']
        if session_coach_id != coach_id:
            return json.dumps({'error': 'Unauthorized to delete this session'}, indent=4, sort_keys=True, default=str), 403

        # Delete the session if it belongs to the coach
        delete_query = "DELETE FROM Session WHERE SessionID = %s"
        cursor.execute(delete_query, (session_id,))
        db.commit()
        return json.dumps({'message': 'Session deleted successfully'}, indent=4, sort_keys=True, default=str), 200

    except Exception as e:
        db.rollback()
        return json.dumps({'error': str(e)}, indent=4, sort_keys=True, default=str), 500

    finally:
        cursor.close()
        db.close()

@session_bp.route('/get_session/<int:session_id>', methods=['GET'])
def get_session_by_id(session_id):
    try:
        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        query = "SELECT SessionID, SessionName, Date, Time, CoachID, ClientID FROM Session WHERE SessionID = %s"
        cursor.execute(query, (session_id,))
        session = cursor.fetchone()

        if session is None:
            return json.dumps({'error': 'Session not found'}, indent=4, sort_keys=True, default=str), 404

        return json.dumps({'session': session}, indent=4, sort_keys=True, default=str), 200

    except Exception as e:
        return json.dumps({'error': str(e)}, indent=4, sort_keys=True, default=str), 500

    finally:
        cursor.close()
        db.close()
