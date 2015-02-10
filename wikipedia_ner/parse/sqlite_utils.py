import sqlite3

def create_schema(conn, schema, table_name):
    symbolic_assignment = ", ".join([name + "=?" for name, row_type in schema])
    symbolic_values = "(" + ", ".join(["?"] * (1 + len(schema))) + ")"

    insert_string = "INSERT into %s values %s"    % (table_name, symbolic_values)
    update_string = "UPDATE %s SET %s WHERE id=?" % (table_name, symbolic_assignment)
    select_string = "SELECT * FROM %s WHERE id=?" % (table_name)
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
            print(obj)

    def update_in_db(obj):
        cursor.execute(update_string,
            obj
        )

    def get_obj_from_db(key):
        cursor.execute(select_string, (key,))
        data = cursor.fetchone()
        return data

    return (insert_into_db, update_in_db, get_obj_from_db)

import .sqlite_prot_buff.corpus_pb2 as corpus_pb2

def convert_legacy_to_protobuff(legacy):
    corpus = corpus_pb2.Corpus()
    for example in legacy:
        ex = corpus.example.add()
        ex.words = example[0]
        triggers = example[1]
        for trigger_id, trigger_text in triggers:
            trig = ex.triggers.add()
            trig.id = trigger_id
            trig.trigger = trigger_text
    return corpus

def deserialize_protobuf(blob):
    corpus = corpus_pb2.Corpus()
    return corpus.ParseFromString(blob)

def serialize_protobuf(corpus):
    return corpus.SerializeToString()
