import sqlite3

def create_schema(conn, schema, table_name):
    symbolic_assignment = ", ".join([name + "=?" for name, row_type in schema])
    symbolic_values = "(" + ", ".join(["?"] * (1 + len(schema))) + ")"

    insert_string = "INSERT into %s values %s"    % (table_name, symbolic_values)
    update_string = "UPDATE %s SET %s WHERE id=?" % (table_name, symbolic_assignment)
    update_string_lines = "UPDATE %s SET lines=? WHERE id=?" % (table_name,)
    select_string = "SELECT * FROM %s WHERE id=?" % (table_name,)
    select_string_lines = "SELECT lines FROM %s WHERE id=?" % (table_name,)
    #lines pickle, parents pickle

    cursor = conn.cursor()
    schema_definition = ", \n".join([name + " " + row_type for name, row_type in schema])

    try:
        cursor.execute("""
            CREATE TABLE %s (
                id    integer primary key not null,
                %s
                )""" % (table_name, schema_definition))
    except sqlite3.OperationalError:
        pass

    def insert_into_db(obj):
        try:
            cursor.execute(
                insert_string,
                obj
            )
            conn.commit()
        except sqlite3.IntegrityError:
            print("Error: sqlite3.IntegrityError => %r" % (obj))

    def update_in_db(obj):
        cursor.execute(update_string,
            obj
        )
        conn.commit()

    def update_lines_in_db(obj):
        cursor.execute(update_string_lines,
            obj
        )
        conn.commit()

    def get_obj_from_db(key):
        cursor.execute(select_string, (key,))
        data = cursor.fetchone()
        return data

    def get_lines_from_db(key):
        cursor.execute(select_string_lines, (key,))
        data = cursor.fetchone()
        return data

    return (insert_into_db, update_in_db, update_lines_in_db, get_obj_from_db, get_lines_from_db)

from .sqlite_proto_buff import corpus_pb2

def convert_examples_to_protobuff(legacy):
    corpus = corpus_pb2.Corpus()
    for example in legacy:
        ex = corpus.example.add()
        ex.words.extend(example[0])
        triggers = example[1]
        for trigger_id, trigger_text in triggers:
            trig = ex.trigger.add()
            trig.id = trigger_id
            trig.trigger = trigger_text
    return corpus

def deserialize_protobuf(blob):
    corpus = corpus_pb2.Corpus()
    corpus.ParseFromString(blob)
    return corpus

def serialize_protobuf(corpus):
    return corpus.SerializeToString()
