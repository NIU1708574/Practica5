import json
from dataclasses import dataclass


@dataclass
class Task:
    id: int
    titol: str
    assignatura: str
    estat: str = "pendent"

    def to_dict(self):
        return {
            "id": self.id,
            "titol": self.titol,
            "assignatura": self.assignatura,
            "estat": self.estat,
        }

    @classmethod
    def from_dict(cls, dades):
        return cls(
            dades["id"],
            dades["titol"],
            dades["assignatura"],
            dades.get("estat", "pendent"),
        )

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, text):
        return cls.from_dict(json.loads(text))
