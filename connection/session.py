import traceback
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, insert, delete, update, func, or_, distinct
from sql.models import engine
from sql.models import (Usuario, Libro, Estado_Libro,
                        Estado_Impresion, Estado_Prestamo, Prestamos,
                        Impresiones, CopiasLibros)


with Session(engine) as session:
    try:
            def select_libros_available(nombre= None, 
                                autor= None, 
                                Editorial= None, 
                                SectorBiblio= None,
                                SectorEstanteria= None, 
                                Estado_= None,
                                offset=None,
                                limit=None):
                try:
                    # Subconsulta: obtener el último préstamo por copia
                    ultimo_prestamo = (
                        select(
                            Prestamos.copia_id,
                            func.max(Prestamos.id_prestamos).label("ultimo_prestamo_id")
                        )
                        .group_by(Prestamos.copia_id)
                        .subquery()
                    )

                    p_alias = aliased(Prestamos)

                    # Comenzamos a construir la consulta
                    query = (
                        select(
                            Libro.nombre_libro,
                            Libro.autor,
                            Libro.editorial,
                            Libro.fecha_entrada,
                            Libro.sector_biblioteca,
                            Libro.sector_estanteria,
                            Estado_Libro.estado_libro,
                            func.count(CopiasLibros.id_copia).label("stock")
                        )
                        .join(CopiasLibros.libro)
                        .join(CopiasLibros.estado)
                        .outerjoin(ultimo_prestamo, CopiasLibros.id_copia == ultimo_prestamo.c.copia_id)
                        .outerjoin(p_alias, p_alias.id_prestamos == ultimo_prestamo.c.ultimo_prestamo_id)
                        .where(
                            or_(
                                p_alias.id_prestamos == None,
                                p_alias.estado_prestamo_id.in_([2, 3])  # Devuelto o Extraviado
                            )
                    ).offset(offset).limit(limit))

                    # Filtros opcionales
                    if nombre:
                        query = query.where(Libro.nombre_libro.ilike(f"%{nombre}%"))
                    if autor:
                        query = query.where(Libro.autor.ilike(f"%{autor}%"))
                    if Editorial:
                        query = query.where(Libro.editorial.ilike(f"%{Editorial}%"))
                    if SectorBiblio:
                        query = query.where(Libro.sector_biblioteca.ilike(f"%{SectorBiblio}%"))
                    if SectorEstanteria:
                        query = query.where(Libro.sector_estanteria.ilike(f"%{SectorEstanteria}%"))
                    if Estado_:
                        query = query.where(Estado_Libro.estado_libro.contains(Estado_))

                    query = query.group_by(
                        Libro.nombre_libro,
                        Libro.autor,
                        Libro.editorial,
                        Libro.sector_biblioteca,
                        Libro.sector_estanteria,
                        Estado_Libro.estado_libro
                    )

                    result = session.execute(query)
                    return result
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print(f"Error {e}")
            def select_libros_equal(nombre, autor, editorial, sectorbiblioteca, sectorestanteria, fecha):
                try:
                    query = (select(Libro)
                            .where(Libro.nombre_libro == nombre)
                            .where(Libro.autor == autor)
                            .where(Libro.editorial == editorial)
                            .where(Libro.sector_biblioteca == sectorbiblioteca)
                            .where(Libro.sector_estanteria == sectorestanteria)
                            .where(Libro.fecha_entrada == fecha))
                        
                    libros = session.execute(query).all()
                    return libros
                except Exception as e:
                    traceback.print_exc()
                    print(f"Error {e}")

            def select_impresion_all(estado=None, papel=None, departamento=None, offset=None, limit=None):
                try:
                    query = (select(Impresiones, Estado_Impresion, Usuario)
                                                .join(Impresiones.estado_impresion)
                                                .join_from(Impresiones, Usuario, Impresiones.user_id == Usuario.id_user))
                    if estado:
                        query = query.where(Impresiones.estado_impresion_id == estado)

                    if papel:
                        query = query.where(Impresiones.tipo_papel == papel)
                    if departamento:
                        query = query.where(Usuario.curso.contains(departamento))
                    
                    query = query.order_by(Impresiones.fecha_impresion.desc())
                    query = query.offset(offset).limit(limit)
                    impresion = session.execute(query).all()
                    return impresion
                except Exception as e:
                    traceback.print_exc()
                    print(f"Error {e}")

            def select_prestamos_all(estado=None, 
                                    rut=None, 
                                    nombre_libro=None,
                                    nombre_user=None,
                                    curso=None,
                                    offset=None,
                                    limit=None):
                try:
                    query = (select(Prestamos.fecha_inicio, Prestamos.fecha_termino, Estado_Prestamo.estado_prestamo,
                                                    Usuario.nombre, Usuario.curso, Usuario.rut, Libro.nombre_libro,
                                                    func.count(Libro.nombre_libro).label("stock"))
                                                    .join(Prestamos.estado_prestamo)
                                                    .join(Prestamos.user)
                                                    .outerjoin(Prestamos.copia)
                                                    .join_from(CopiasLibros, Libro, CopiasLibros.libro_id == Libro.id_libro)
                                                    .group_by(Usuario.nombre, Libro.nombre_libro,Prestamos.fecha_inicio, Estado_Prestamo.estado_prestamo)
                                                    .order_by(Prestamos.fecha_inicio.desc()))
                    if estado:
                        query = query.where(Prestamos.estado_prestamo_id == estado)
                    if rut:
                        query = query.where(Usuario.rut.contains(rut))
                    if nombre_libro:
                        query = query.where(Libro.nombre_libro.contains(nombre_libro))
                    if nombre_user:
                        query = query.where(Usuario.nombre.contains(nombre_user))
                    if curso:
                        query = query.where(Usuario.curso.contains(curso))
                    query = query.offset(offset).limit(limit)
                    prestamos = session.execute(query)
                    return prestamos
                except Exception as e:
                    traceback.print_exc()
                    print(f"Errores {e}")

            def selected_user_by_rut(rut_):
                try:
                    user = session.execute(select(Usuario).where(Usuario.rut == rut_)).all()
                    return user
                except Exception as e:
                    traceback.print_exc()
                    print(f"Error {e}")

            def select_estado_libro_all():
                try:
                    estado_libro = session.execute(select(Estado_Libro)).all()
                    return estado_libro

                except Exception as e:
                    traceback.print_exc()
                    print(f"Errores {e}")

            def select_copia_libros_by_id(id):
                try:
                    # Subconsulta: último préstamo por copia
                    ultimo_prestamo = (
                        select(
                            Prestamos.copia_id,
                            func.max(Prestamos.id_prestamos).label("ultimo_prestamo_id")
                        )
                        .group_by(Prestamos.copia_id)
                        .subquery()
                    )

                    # Alias para Prestamos
                    p_alias = aliased(Prestamos)

                    # Consulta principal
                    libros = session.execute(
                        select(
                            CopiasLibros.id_copia,
                            Libro.nombre_libro,
                            Libro.autor,
                            Libro.editorial,
                            Libro.fecha_entrada,
                            Estado_Libro.estado_libro
                        )
                        .join(CopiasLibros.libro)
                        .join(CopiasLibros.estado)
                        .outerjoin(ultimo_prestamo, CopiasLibros.id_copia == ultimo_prestamo.c.copia_id)
                        .outerjoin(p_alias, p_alias.id_prestamos == ultimo_prestamo.c.ultimo_prestamo_id)
                        .where(CopiasLibros.libro_id == id)
                        .where(
                            or_(
                                p_alias.id_prestamos == None,  # nunca ha sido prestado
                                p_alias.estado_prestamo_id.in_([2, 3])  # Devuelto o Extraviado
                            )
                        )
                    ).all()
                    return libros

                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print(f"Error {e}")

            def select_prestamo_by_fecha(fecha):
                try:
                    prestamo_fecha = session.execute(select(Usuario.nombre, Libro.nombre_libro, Libro.editorial, Libro.autor,
                                                            Prestamos.fecha_inicio, Prestamos.fecha_termino,
                                                            Estado_Libro.estado_libro, CopiasLibros.id_copia, Prestamos.id_prestamos)
                                                            .join(Prestamos.copia)
                                                            .join(Prestamos.user)
                                                            .join_from(CopiasLibros, Libro, CopiasLibros.libro_id == Libro.id_libro)
                                                            .join_from(CopiasLibros, Estado_Libro, CopiasLibros.estado_id == Estado_Libro.id_estadolibro)
                                                            .outerjoin(Prestamos.estado_prestamo)
                                                            .where(Prestamos.fecha_inicio.contains(fecha))
                                                            .where(or_(Estado_Prestamo.estado_prestamo == "Prestado",
                                                                    Estado_Prestamo.estado_prestamo == "Extraviado")))
                    return prestamo_fecha
                except Exception as e:
                    traceback.print_exc()
                    print(f"Error {e}")

            def select_prestamo_libro(nombre, autor, editorial):
                try:
                    # Subconsulta: último préstamo por copia
                    ultimo_prestamo = (
                        select(
                            Prestamos.copia_id,
                            func.max(Prestamos.id_prestamos).label("ultimo_prestamo_id")
                        )
                        .group_by(Prestamos.copia_id)
                        .subquery()
                    )

                    # Alias para Prestamos
                    p_alias = aliased(Prestamos)

                    # Datos de prestamos
                    prestamos = session.execute(select(Libro.nombre_libro, Libro.autor, Libro.editorial,
                                                    Libro.fecha_entrada, Estado_Libro.estado_libro, CopiasLibros.id_copia,
                                                    Libro.id_libro)
                                                    .join(Libro.copias)
                                                    .join(CopiasLibros.estado)
                                                    .outerjoin(ultimo_prestamo, CopiasLibros.id_copia == ultimo_prestamo.c.copia_id)
                                                    .outerjoin(p_alias, p_alias.id_prestamos == ultimo_prestamo.c.ultimo_prestamo_id)
                                                    .where(Libro.nombre_libro == nombre)
                                                    .where(Libro.autor == autor)
                                                    .where(Libro.editorial == editorial)
                                                    .where(
                                                            or_(
                                                                    p_alias.id_prestamos == None,  # nunca ha sido prestado
                                                                    p_alias.estado_prestamo_id.in_([2, 3])  # Devuelto o Extraviado
                                                                )
                                                            )
                                                    .order_by(Libro.fecha_entrada.desc())).all()
                    return prestamos
                except Exception as e:
                    traceback.print_exc()
                    print(f"Error {e}")

            def select_cursos_user():
                try:
                    curso = session.execute(select(distinct(Usuario.curso)))
                    return curso
                except Exception as e:
                    traceback.print_exc()
                    print(f"Error {e}")
            def select_all_estado_prestamos():
                try:
                    estado = session.execute(select(Estado_Prestamo)).all()
                    return estado
                except Exception as e:
                    traceback.print_exc()
                    print(f"Error {e}")

            def select_all_estado_impresion():
                try:
                    estado = session.execute(select(Estado_Impresion)).all()
                    return estado
                except Exception as e:
                    traceback.print_exc()
                    print(f"Errores {e}")

            def select_type_sheet():
                try:
                    hoja = session.execute(select(distinct(Impresiones.tipo_papel)))
                    return hoja
                except Exception as e:
                    traceback.print_exc()
                    print(f"Error {e}")

    except Exception as e:
        traceback.print_exc()
        print(f"Error {e}")
    finally:
        session.close()