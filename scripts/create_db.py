from application.dependencies.database import Base, engine


def create_tables():
    print("Start create tables")
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    create_tables()
