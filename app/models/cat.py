from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Cat(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    color: Mapped[str] 
    personality: Mapped[str] 