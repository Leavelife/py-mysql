from flask import Blueprint, request, jsonify
from db import get_db_connection

bp = Blueprint('tugas', __name__, url_prefix='/tugas')

@bp.route('/add', methods=['POST'])
def add_tugas():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = '''
        INSERT INTO tugas (NIM, judul, link_dokumen, kode_mk)
        VALUES (%s, %s, %s, %s)
    '''
    cursor.execute(query, (data['NIM'], data['judul'], data['link_dokumen'], data['kode_mk']))
    conn.commit()
    conn.close()
    print("data : ", data)
    return jsonify({'message': 'Tugas ditambahkan'}), 201