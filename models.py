from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Publisher(Base):
    __tablename__ = "publisher"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Publisher(id={self.id!r}, name={self.name!r})"


class Shop(Base):
    __tablename__ = "shop"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Shop(id={self.id!r}, name={self.name!r})"


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    id_publisher: Mapped[int] = mapped_column(ForeignKey("publisher.id"))
    publisher: Mapped["Publisher"] = relationship(Publisher, backref="book")

    def __repr__(self) -> str:
        return f"Book(id={self.id!r}, title={self.title!r}, \
        id_publisher={self.id_publisher!r}, publisher={self.publisher!r})"


class Stock(Base):
    __tablename__ = "stock"

    id: Mapped[int] = mapped_column(primary_key=True)
    count: Mapped[int] = mapped_column(Integer)
    id_book: Mapped[int] = mapped_column(ForeignKey("book.id"))
    id_shop: Mapped[int] = mapped_column(ForeignKey("shop.id"))

    book: Mapped["Book"] = relationship(Book, backref="stock")
    shop: Mapped["Shop"] = relationship(Shop, backref="shop")

    def __repr__(self) -> str:
        return f"Stock(id={self.id!r}, count={self.count!r}, id_book={self.id_book!r}, id_shop={self.id_shop!r})"


class Sale(Base):
    __tablename__ = "sale"

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[float] = mapped_column(Float)
    date_sale: Mapped[datetime] = mapped_column(DateTime)
    count: Mapped[int] = mapped_column(Integer)
    id_stock: Mapped[int] = mapped_column(ForeignKey("stock.id"))

    stock: Mapped["Stock"] = relationship(Stock, backref="sale")

    def __repr__(self) -> str:
        return f"Sale(id={self.id!r}, price={self.price!r}, date_sale={self.date_sale!r}, \
        count={self.count!r}, id_stock={self.id_stock!r})"
