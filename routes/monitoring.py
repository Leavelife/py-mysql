from flask import Blueprint, request, jsonify
from db import get_db_connection

bp = Blueprint('monitoring', __name__, url_prefix='/monitoring')

@bp.route('/add', methods=['POST'])
def add_monitoring():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = '''
        INSERT INTO monitoring_tugas (id_tugas, status, komentar, NIDN)
        VALUES (%s, %s, %s, %s)
    '''
    cursor.execute(query, (
        data['id_tugas'],
        data['status'],
        data['komentar'],
        data['NIDN']
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Monitoring ditambahkan'}), 201

@bp.route('/list', methods=['GET'])
def list_tugas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = '''
        SELECT * FROM v_monitoring_tugas;
    '''
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return jsonify(result)

@bp.route('/update/<int:id_tugas>', methods=['PUT'])
def update_monitoring(id_tugas):
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.callproc("sp_periksa_tugas", (
            id_tugas,
            data["NIDN"],
            data["komentar"]
        ))

        conn.commit()
        return jsonify({"message": f"Monitoring untuk tugas ID {id_tugas} diperbarui"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
