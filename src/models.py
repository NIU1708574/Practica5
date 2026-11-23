import json
from dataclasses import dataclass


@dataclass
class Task:
    id: int
    titol: str
    assignatura: str
    estat: str = "pendent"
    data_limit: str | None = None

    def to_dict(self):
        dades = {
            "id": self.id,
            "titol": self.titol,
            "assignatura": self.assignatura,
            "estat": self.estat,
        }
        if self.data_limit is not None:
            dades["data_limit"] = self.data_limit
        return dades

    @classmethod
    def from_dict(cls, dades):
        return cls(
            dades["id"],
            dades["titol"],
            dades["assignatura"],
            dades.get("estat", "pendent"),
            dades.get("data_limit"),
        )

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, text):
        return cls.from_dict(json.loads(text))
