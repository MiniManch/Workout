from flask import Blueprint, jsonify, request
import json
from data.setup_db import get_db_connection
import pymysql
from datetime import timedelta

session_bp = Blueprint('session', __name__, url_prefix='/session')

@session_bp.route('/coach/<int:coach_id>', methods=['GET'])
def get_sessions_by_coach(coach_id):
    try:
        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
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
            for session in sessions:
                session['Duration'] = str(session['Duration'])
            return json.dumps({'sessions': sessions}, indent=4, sort_keys=True, default=str), 200
        else:
            return json.dumps({'message': 'No sessions found for this coach'}, indent=4, sort_keys=True, default=str), 404
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return json.dumps({'error': str(e)}, indent=4, sort_keys=True, default=str), 500

@session_bp.route('/coach/<int:coach_id>', methods=['POST'])
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

        insert_session_query = "INSERT INTO Session (SessionName, Date, StartTime, CoachID, Duration) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_session_query, (name, date, time, coach_id, duration))
        db.commit()
        session_id = cursor.lastrowid

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

@session_bp.route('/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        data = request.get_json()
        new_name = data.get('SessionName')
        new_date = data.get('Date')
        new_time = data.get('StartTime')
        new_duration = data.get('Duration')
        new_client_id = data.get('ClientID')

        update_session_query = "UPDATE Session SET SessionName = %s, Date = %s, StartTime = %s, Duration = %s WHERE SessionID = %s"
        cursor.execute(update_session_query, (new_name, new_date, new_time, new_duration, session_id))

        update_client_query = "UPDATE SessionClient SET ClientID = %s WHERE SessionID = %s"
        cursor.execute(update_client_query, (new_client_id, session_id))

        db.commit()
        return json.dumps({'message': 'Session updated successfully'}, indent=4, sort_keys=True, default=str), 200

    except Exception as e:
        db.rollback()
        print(str(e))
        return json.dumps({'error': str(e)}, indent=4, sort_keys=True, default=str), 500

    finally:
        cursor.close()
        db.close()

@session_bp.route('/<int:session_id>/coach/<int:coach_id>', methods=['DELETE'])
def delete_session(coach_id, session_id):
    try:
        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        check_query = "SELECT CoachID FROM Session WHERE SessionID = %s"
        cursor.execute(check_query, (session_id,))
        result = cursor.fetchone()

        if result is None:
            return json.dumps({'error': 'Session not found'}, indent=4, sort_keys=True, default=str), 404

        session_coach_id = result['CoachID']
        if session_coach_id != coach_id:
            return json.dumps({'error': 'Unauthorized to delete this session'}, indent=4, sort_keys=True, default=str), 403

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

@session_bp.route('/<int:session_id>/coach/<int:coach_id>', methods=['GET'])
def get_session_by_id(session_id, coach_id):
    try:
        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        
        query = """
            SELECT s.SessionID, s.SessionName, s.Date, s.StartTime, s.CoachID, s.Duration, sc.ClientID
            FROM Session AS s
            LEFT JOIN SessionClient AS sc ON s.SessionID = sc.SessionID
            WHERE s.SessionID = %s AND s.CoachID = %s
        """
        
        cursor.execute(query, (session_id, coach_id))
        session = cursor.fetchone()

        if session is None:
            return json.dumps({'error': 'Session not found for this coach'}, indent=4, sort_keys=True, default=str), 404

        return json.dumps({'session': session}, indent=4, sort_keys=True, default=str), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return json.dumps({'error': str(e)}, indent=4, sort_keys=True, default=str), 500

    finally:
        cursor.close()
        db.close()

@session_bp.route('/client/<int:client_id>', methods=['GET'])
def get_client_sessions(client_id):
    try:
        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        query = """
            SELECT s.SessionID, s.SessionName, s.Date, s.StartTime, s.CoachID, s.Duration, sc.ClientID
            FROM Session AS s
            LEFT JOIN SessionClient AS sc ON s.SessionID = sc.SessionID
            WHERE sc.ClientID = %s
        """
        cursor.execute(query, (client_id,))
        sessions = cursor.fetchall()

        if sessions:
            for session in sessions:
                session['Duration'] = str(session['Duration'])
            return json.dumps({'sessions': sessions}, indent=4, sort_keys=True, default=str), 200
        else:
            return json.dumps({'message': 'No sessions found for this client','sessions':[]}, indent=4, sort_keys=True, default=str), 404

    except Exception as e:
        print(str(e))
        return json.dumps({'error': str(e)}, indent=4, sort_keys=True, default=str), 500

    finally:
        cursor.close()
        db.close()
