from flask import Blueprint, request, jsonify
from db import get_db_connection

bp = Blueprint('mahasiswa', __name__, url_prefix='/mahasiswa')

@bp.route('/add', methods=['POST'])
def add_mahasiswa():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO mahasiswa (NIM, nama_mhs, kelas) VALUES (%s, %s, %s)"
    cursor.execute(query, (data['NIM'], data['nama_mhs'], data['kelas']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Mahasiswa ditambahkan'}), 201
