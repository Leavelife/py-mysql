from flask import Flask
from routes import tugas, monitoring

app = Flask(__name__)

# Register blueprint
app.register_blueprint(tugas.bp)
app.register_blueprint(monitoring.bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
