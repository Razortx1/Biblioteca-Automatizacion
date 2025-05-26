import os
from datetime import date
import sqlite3
import shutil

# Funcion para backups solo de sqlite3. Si implementa otro motor, no es necesario
def backups_database_rotation(max_backups = 3):
    """
    **Funcion backups_database_rotation**\n
    Permite la copia de seguridad para archivos sqlite3, con un maximo de 3 archivos

    **Parametros**\n
    max_backups: int = 3
    """
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

    
def backups_restoration(backup_filename):
    """
    **backups_restoration**\n
    Permite el poder restaurar un backup

    **Parametros**\n
    backup_filename: str
    """
    from main import resource_path
    from sqlalchemy.orm import close_all_sessions
    close_all_sessions()

    db_path = resource_path("sql/biblioteca.db")
    print(db_path)
    backup_path = resource_path(f"backups/{backup_filename}")
    print(backup_path)

    if os.path.exists(backup_path):
        shutil.copy2(backup_path, db_path)
        return True
    else:
        return False
