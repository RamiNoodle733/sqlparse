import sqlparse


def test_split_redshift_begin_read_write():  # issue843
    sql = """BEGIN READ WRITE;
DELETE FROM schema.table_a USING table_a_temp
WHERE schema.table_a.id = table_a_temp.id;
INSERT INTO schema.table_a SELECT * FROM table_a_temp;
END TRANSACTION;
"""

    statements = sqlparse.split(sql)

    assert len(statements) == 4
    assert statements[0] == 'BEGIN READ WRITE;'
    assert statements[1].startswith('DELETE FROM schema.table_a')
    assert statements[2].startswith('INSERT INTO schema.table_a')
    assert statements[3] == 'END TRANSACTION;'
