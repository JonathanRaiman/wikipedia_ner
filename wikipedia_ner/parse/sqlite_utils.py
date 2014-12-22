import sqlite3

def create_schema(cursor, schema, table_name):
    symbolic_assignment = ", ".join([name + "=?" for name, row_type in schema])
    symbolic_values = "(" + ", ".join(["?"] * (1 + len(schema))) + ")"

    insert_string = "INSERT into %s values %s"    % (table_name, symbolic_values)
    update_string = "UPDATE %s SET %s WHERE id=?" % (table_name, symbolic_assignment)
    select_string = "SELECT * FROM %s WHERE id=?" % (table_name)
    #lines pickle, parents pickle

    schema_definition = ", \n".join([name + " " + row_type for name, row_type in schema])

    try:
        cursor.execute("""
            CREATE TABLE %s (
                id    integer primary key not null,
                %s
                )""" % (table_name, schema_definition))
    except sqlite3.OperationalError:
        pass

    def insert_into_db(cursor, obj):
        cursor.execute(
            insert_string,
            obj
        )
        sqlite3.IntegrityError
        cursor.commit()

    def update_in_db(cursor, obj):
        cursor.execute(update_string,
            obj
        )

    def get_obj_from_db(cursor, key):
        cursor.execute(select_string, (key))
        data = cursor.fetchone()
        return data

    return (insert_into_db, update_in_db, get_obj_from_db)



