from flask import Flask
import psycopg2
import os

app = Flask(__name__)

VERSION = "2.0.0"

@app.route("/")
def inicio():
    try:
        # Conexión al servicio de base de datos en la red de docker-compose
        conexion = psycopg2.connect(
            host=os.environ.get("DB_HOST", "db"),
            database=os.environ.get("DB_NAME", "empresa"),
            user=os.environ.get("DB_USER", "admin"),
            password=os.environ.get("DB_PASSWORD", "admin123")
        )

        cursor = conexion.cursor()

        # Obtener versión de PostgreSQL
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]

        # Consultar clientes de la tabla 'clientes' (Actividad 5)
        clientes_html = ""
        try:
            cursor.execute("SELECT id, nombre FROM clientes ORDER BY id;")
            clientes = cursor.fetchall()
            if clientes:
                clientes_html += "<h3>Listado de Clientes Registrados:</h3><ul>"
                for cliente in clientes:
                    clientes_html += f"<li><strong>ID:</strong> {cliente[0]} | <strong>Nombre:</strong> {cliente[1]}</li>"
                clientes_html += "</ul>"
            else:
                clientes_html = "<p><em>No hay clientes registrados en la tabla 'clientes' todavía.</em></p>"
        except psycopg2.errors.UndefinedTable:
            # Revertir la transacción fallida por falta de tabla
            conexion.rollback()
            clientes_html = (
                "<p style='color: #ffa500;'><strong>Aviso:</strong> La tabla 'clientes' no existe en la base de datos.</p>"
                "<p>Para cumplir con la <strong>Actividad 3 y 4</strong>, conéctese a pgAdmin en <a href='http://localhost:8080' target='_blank'>http://localhost:8080</a> "
                "y ejecute el siguiente comando SQL:</p>"
                "<pre><code>CREATE TABLE clientes(\n    id SERIAL PRIMARY KEY,\n    nombre VARCHAR(100)\n);\n\n"
                "INSERT INTO clientes (nombre) VALUES ('Cliente A'), ('Cliente B'), ('Cliente C');</code></pre>"
            )
        except Exception as table_err:
            conexion.rollback()
            clientes_html = f"<p style='color: red;'>Error al consultar clientes: {str(table_err)}</p>"

        cursor.close()
        conexion.close()

        # Retornar interfaz moderna y estética (según directrices de UI Premium)
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Aplicación Flask - DevOps Taller</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
                    color: #f3f4f6;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                }}
                .container {{
                    background: rgba(31, 41, 55, 0.6);
                    backdrop-filter: blur(12px);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 20px;
                    padding: 40px;
                    max-width: 600px;
                    width: 90%;
                    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
                    text-align: center;
                }}
                h1 {{
                    font-size: 2.2rem;
                    margin-top: 0;
                    margin-bottom: 10px;
                    background: linear-gradient(to right, #38bdf8, #3b82f6);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }}
                h2 {{
                    font-size: 1.05rem;
                    color: #9ca3af;
                    margin-bottom: 30px;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    font-weight: 500;
                }}
                h3 {{
                    color: #38bdf8;
                    text-align: left;
                    margin-top: 25px;
                    font-weight: 600;
                }}
                .status-box {{
                    background: rgba(16, 185, 129, 0.1);
                    border-left: 4px solid #10b981;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: left;
                    margin-bottom: 25px;
                    font-size: 0.95rem;
                }}
                .version-tag {{
                    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
                    color: #fff;
                    padding: 4px 10px;
                    border-radius: 9999px;
                    font-size: 0.8rem;
                    vertical-align: middle;
                    margin-left: 8px;
                    font-weight: 600;
                    box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
                }}
                ul {{
                    text-align: left;
                    padding-left: 0;
                    line-height: 1.6;
                    margin: 0;
                }}
                li {{
                    margin-bottom: 10px;
                    background: rgba(255, 255, 255, 0.03);
                    padding: 10px 16px;
                    border-radius: 8px;
                    list-style-type: none;
                    border-left: 3px solid #3b82f6;
                    display: flex;
                    justify-content: space-between;
                    border: 1px solid rgba(255, 255, 255, 0.05);
                    border-left-width: 4px;
                    border-left-color: #3b82f6;
                }}
                pre {{
                    background: #111827;
                    color: #a7f3d0;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: left;
                    overflow-x: auto;
                    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
                    font-size: 0.85rem;
                    border: 1px solid rgba(255, 255, 255, 0.05);
                }}
                a {{
                    color: #38bdf8;
                    text-decoration: none;
                    font-weight: 500;
                    transition: color 0.2s;
                }}
                a:hover {{
                    color: #7dd3fc;
                }}
                footer {{
                    margin-top: 40px;
                    font-size: 0.8rem;
                    color: rgba(156, 163, 175, 0.6);
                    border-top: 1px solid rgba(255, 255, 255, 0.05);
                    padding-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Aplicación Flask <span class="version-tag">v{VERSION}</span></h1>
                <h2>Taller Práctico de DevOps</h2>
                
                <div class="status-box">
                    <p style="margin: 0; font-weight: 600; color: #34d399; display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.2rem;">●</span> Conexión exitosa a PostgreSQL
                    </p>
                    <p style="margin: 8px 0 0 0; font-size: 0.85rem; color: #9ca3af; word-break: break-all;">{db_version}</p>
                </div>
                
                <div style="margin-top: 10px;">
                    {clientes_html}
                </div>
                
                <footer>
                    Desarrollado para el taller de Docker Compose y CI/CD
                </footer>
            </div>
        </body>
        </html>
        """

    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Error de Conexión - DevOps Taller</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #0f172a;
                    color: #f87171;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                .error-container {{
                    background: #1e293b;
                    border: 1px solid #ef4444;
                    padding: 40px;
                    border-radius: 12px;
                    max-width: 500px;
                    width: 90%;
                    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
                }}
                h1 {{
                    margin-top: 0;
                    font-size: 1.5rem;
                    color: #ef4444;
                }}
                pre {{
                    background: #0f172a;
                    color: #fca5a5;
                    padding: 15px;
                    border-radius: 6px;
                    overflow-x: auto;
                    font-size: 0.85rem;
                    border: 1px solid rgba(239, 68, 68, 0.2);
                }}
            </style>
        </head>
        <body>
            <div class="error-container">
                <h1>✗ Error de Conexión a la Base de Datos</h1>
                <p>No se pudo conectar a PostgreSQL en el host '{os.environ.get("DB_HOST", "db")}'.</p>
                <p><strong>Detalle del error:</strong></p>
                <pre>{str(e)}</pre>
                <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 20px;">
                    Asegúrese de levantar los servicios con <code>docker compose up -d</code> y que el contenedor <code>postgresdb</code> esté en ejecución.
                </p>
            </div>
        </body>
        </html>
        """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
