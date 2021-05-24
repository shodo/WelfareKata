import contextlib
from unittest import TestCase

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker


def get_engine():
    path = __file__
    main_path = path.split("/welfarekata/webapp")[0]

    engine = create_engine(f"sqlite:///{main_path}/welfarekata/webapp/test/test_db.sqlite3")
    return engine


def get_test_session_factory(engine):
    session_factory = sessionmaker()
    session_factory.configure(bind=engine)

    return session_factory


def clear_db_data(engine):
    meta = MetaData()
    meta.reflect(bind=engine)

    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(meta.sorted_tables):
            con.execute(table.delete())
        trans.commit()


class SqlAlchemyTestCase(TestCase):
    def setUp(self) -> None:
        self.engine = get_engine()
        self.session_factory = get_test_session_factory(self.engine)
        clear_db_data(self.engine)

    def tearDown(self) -> None:
        clear_db_data(self.engine)
