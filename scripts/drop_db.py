from application.dependencies.database import Base, engine
from application.infrastructure.model import country


def drop_tables():
    Base.metadata.drop_all(bind=engine)


if __name__ == '__main__':
    drop_tables()
