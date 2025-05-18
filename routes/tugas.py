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
    return jsonify({'message': 'Tugas ditambahkan'}), 201

@bp.route('/by_nim/<nim>', methods=['GET'])
def get_tugas_by_nim(nim):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_tugas FROM tugas WHERE NIM = %s", (nim,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify(result), 200
    else:
        return jsonify({"message": "Data tidak ditemukan"}), 404

@bp.route('/delete/<id_tugas>', methods=['DELETE'])
def delete_tugas(id_tugas):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tugas WHERE id_tugas = %s", (id_tugas,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Tugas dengan ID {id_tugas} dihapus"}), 200

@bp.route('/update/<nim>', methods=['PUT'])
def update_tugas(nim):
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()

    try:
        # Gunakan nim sebagai identifikasi, tapi jangan update NIM-nya juga
        cursor.execute("""
            UPDATE tugas SET 
                judul = %s,
                link_dokumen = %s,
                kode_mk = %s
            WHERE NIM = %s
        """, (data["judul"], data["link_dokumen"], data["kode_mk"], nim))

        conn.commit()
        return jsonify({"message": "Data tugas berhasil diupdate"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
