from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', 'root'),
        database=os.environ.get('DB_NAME', 'holamundo')
    )

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>App con MySQL</title>
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                color: white;
            }
            .container {
                background: rgba(0,0,0,0.7);
                border-radius: 20px;
                padding: 40px;
                text-align: center;
                box-shadow: 0 0 30px rgba(0,0,0,0.5);
            }
            h1 { font-size: 3em; margin-bottom: 10px; }
            .status { margin-top: 20px; font-size: 1.2em; }
            .connected { color: #4ade80; }
            .error { color: #f87171; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Hola Mundo DevOps</h1>
            <p>Aplicación conectada a MySQL</p>
            <div class="status">
                <a href="/db-test">➡️ Probar conexión a BD</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/db-test')
def db_test():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 'Conexión exitosa a MySQL!' as mensaje, NOW() as hora")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test BD</title>
            <style>
                body {{
                    background: #0d0d0d;
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    color: #e0e0e0;
                }}
                .panel {{
                    background: #1a1a2e;
                    border-radius: 20px;
                    padding: 40px;
                    text-align: center;
                    border: 1px solid #b14eff;
                    max-width: 500px;
                }}
                h1 {{ color: #b14eff; }}
                .exito {{ color: #4ade80; font-size: 1.2em; margin: 20px 0; }}
                .hora {{ margin-top: 20px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="panel">
                <h1>✅ Conexión Exitosa</h1>
                <div class="exito">📊 {result[0]}</div>
                <div class="hora">🕒 {result[1]} UTC</div>
                <br>
                <a href="/" style="color: #b14eff;">⬅️ Volver</a>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error BD</title>
            <style>
                body {{
                    background: #0d0d0d;
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                .panel {{
                    background: #1a1a2e;
                    border-radius: 20px;
                    padding: 40px;
                    text-align: center;
                    border: 1px solid #f87171;
                    max-width: 500px;
                    color: white;
                }}
                h1 {{ color: #f87171; }}
                .error {{ color: #f87171; }}
            </style>
        </head>
        <body>
            <div class="panel">
                <h1>❌ Error de Conexión</h1>
                <div class="error">{str(e)}</div>
                <br>
                <a href="/" style="color: #b14eff;">⬅️ Volver</a>
            </div>
        </body>
        </html>
        """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)