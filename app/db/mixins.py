from app.db.core import Base


class ReprMixin:
    def __repr__(self) -> str:
        assert isinstance(self, Base)
        assert issubclass(self.__class__, Base)

        repr_ignore = getattr(self, "__repr_ignore__", [])
        fields = ", ".join(
            f"{col}={repr(getattr(self, col))}"
            for col in self.__mapper__.columns.keys()
            if col not in repr_ignore
        )
        return f"<{self.__class__.__name__}({fields})>"
