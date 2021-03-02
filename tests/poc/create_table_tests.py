# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_quick_guide.htm
from sqlalchemy import MetaData, Integer
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.dml import Insert
from sqlalchemy.sql.schema import Column, Table
from sqlalchemy.sql.sqltypes import String

# engine = create_engine("sqlite:///college.db", echo=True)
meta = MetaData()

students = Table(
    "students",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("lastname", String),
)


def test_single_insert():
    engine = create_engine("sqlite:///:memory:", echo=True)
    meta.create_all(engine)

    ins = students.insert().values(name="Karan")
    conn = engine.connect()
    result = conn.execute(ins)
    assert result.is_insert is True
    assert result.inserted_primary_key == [1]


def test_multi_inserts():
    engine = create_engine("sqlite:///:memory:", echo=True)
    meta.create_all(engine)

    conn = engine.connect()
    conn.execute(
        students.insert(),
        [
            {"name": "Rajiv", "lastname": "Khanna"},
            {"name": "Komal", "lastname": "Bhandari"},
            {"name": "Abdul", "lastname": "Sattar"},
            {"name": "Priya", "lastname": "Rajhans"},
        ],
    )

    result = conn.execute(students.select())

    assert list(map(lambda x: x.name, result)) == [
        "Rajiv",
        "Komal",
        "Abdul",
        "Priya",
    ]
