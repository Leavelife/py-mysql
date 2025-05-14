from flask import Blueprint, request, jsonify
from db import get_db_connection

bp = Blueprint('tugas', __name__, url_prefix='/tugas')

@bp.route('/add', methods=['POST'])
def add_tugas():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = '''
        INSERT INTO tugas (NIM, judul, kode_mk)
        VALUES (%s, %s, %s)
    '''
    cursor.execute(query, (data['NIM'], data['judul'], data['kode_mk']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Tugas ditambahkan'}), 201

@bp.route('/all', methods=['GET'])
def get_all_tugas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tugas")
    result = cursor.fetchall()
    conn.close()
    return jsonify(result)
