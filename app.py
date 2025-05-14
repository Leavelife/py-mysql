from flask import Flask
from routes import mahasiswa, tugas, monitoring

app = Flask(__name__)

# Register blueprint
app.register_blueprint(mahasiswa.bp)
app.register_blueprint(tugas.bp)
app.register_blueprint(monitoring.bp)

if __name__ == '__main__':
    app.run(debug=True)
