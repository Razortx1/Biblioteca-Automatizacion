import os
from datetime import date
import sqlite3

# Funcion para backups solo de sqlite3. Si implementa otro motor, no es necesario
def backups_database_rotation(max_backups = 3):
    from main import resource_path
    dir = resource_path("backups")
    os.makedirs(dir, exist_ok=True)

    timestamp = date.today().strftime("%Y-%m-%d")
    backup_filename = f"backup_{timestamp}.db"
    backup_path = os.path.join(dir, backup_filename)

    db_path = resource_path("sql/biblioteca.db")

    src_conn = sqlite3.connect(db_path)
    dest_conn = sqlite3.connect(backup_path)
    with dest_conn:
        src_conn.backup(dest_conn)

    src_conn.close()
    dest_conn.close()

    backups = sorted(
        [f for f in os.listdir(dir) if f.startswith("backup_") and f.endswith(".db")],
        key = lambda name: os.path.getmtime(os.path.join(dir, name))
    )

    while len(backups) > max_backups:
        to_delete = backups.pop(0)
        os.remove(os.path.join(dir, to_delete))

    

