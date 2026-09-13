import sqlparse


def test_split_oracle_procedure_with_declarations():
    sql = """CREATE PROCEDURE remove_emp (employee_id NUMBER) AS
   tot_emps NUMBER;
   BEGIN
      DELETE FROM employees
      WHERE employees.employee_id = remove_emp.employee_id;
   tot_emps := tot_emps - 1;
   END;"""

    statements = sqlparse.split(sql)

    assert len(statements) == 1
    assert statements[0] == sql


def test_split_oracle_procedure_then_statement():
    sql = """CREATE OR REPLACE PROCEDURE update_counter AS
   counter NUMBER;
   label VARCHAR2(20);
BEGIN
   counter := 1;
   label := 'ready';
END;
SELECT 42;"""

    statements = sqlparse.split(sql)

    assert len(statements) == 2
    assert statements[0].endswith("END;")
    assert statements[1] == "SELECT 42;"
