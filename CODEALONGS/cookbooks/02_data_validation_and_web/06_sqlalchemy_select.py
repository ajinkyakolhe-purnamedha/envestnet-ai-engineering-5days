# SQLAlchemy select
from sqlalchemy import Float, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

class Base(DeclarativeBase):
    pass

class Price(Base):
    __tablename__ = "prices"
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
with Session(engine) as session:
    session.add(Price(symbol="SPY", price=228.80))
    session.commit()
    result = session.scalar(select(Price).where(Price.symbol == "SPY"))
    print(result.price)

