import json
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Base, Publisher, Shop, Book, Stock, Sale
from dotenv import dotenv_values
from tabulate import tabulate


if __name__ == "__main__":
    env = dotenv_values(".env")
    DSN = f"postgresql://{env['USERNAME']}:{env['PASSWORD']}@{env['DB_HOSTNAME']}:{env['DB_PORT']}/{env['DB_NAME']}"
    id_publisher = 1

    engine = create_engine(DSN, echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with open("fixtures/tests_data.json", "r") as f:
        data = json.load(f)

    records = []
    for record in data:
        model = {
            "publisher": Publisher,
            "shop": Shop,
            "book": Book,
            "stock": Stock,
            "sale": Sale,
        }[record.get("model")]
        records.append(model(id=record.get("pk"), **record.get("fields")))

    with Session(engine) as session:
        session.add_all(records)
        session.commit()
        table = []
        stmt = (
            select(Book.title, Shop.name, Sale.price, Sale.date_sale)
            .select_from(Publisher)
            .join(Book, Book.id_publisher == Publisher.id)
            .join(Stock, Stock.id_book == Book.id)
            .join(Sale, Sale.id_stock == Stock.id)
            .join(Shop, Shop.id == Stock.id_shop)
            .where(Book.id_publisher == id_publisher)
        )
        for book in session.execute(stmt):
            table.append(book)
        print(
            tabulate(
                table,
                headers=["Book.title", "Shop.name", "Sale.price", "Sale.date_sale"],
                tablefmt="fancy_outline",
            )
        )
