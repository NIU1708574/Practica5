import argparse
import json
import re
from datetime import date
from pathlib import Path

try:
    from models import Task
except ImportError:
    from src.models import Task


def fitxer_tasques():
    return Path(__file__).resolve().parent.parent / "data" / "tasks.json"


def desar_tasques(tasques):
    fitxer = fitxer_tasques()
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    fitxer.write_text(
        json.dumps(
            [tasca.to_dict() for tasca in tasques],
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def carregar_tasques():
    fitxer = fitxer_tasques()
    if not fitxer.exists():
        desar_tasques([])
        return []
    try:
        dades = json.loads(fitxer.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return []
    if not isinstance(dades, list):
        return []
    return [Task.from_dict(registre) for registre in dades]


FORMAT_DATA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def es_data_valida(valor):
    if not valor or not FORMAT_DATA.fullmatch(valor):
        return False
    try:
        date.fromisoformat(valor)
    except ValueError:
        return False
    return True


def afegir_tasca(titol, assignatura, data_limit):
    if not es_data_valida(data_limit):
        print("error: fecha invalida")
        return

    tasques = carregar_tasques()
    nou_id = max((tasca.id for tasca in tasques), default=0) + 1
    tasca = Task(nou_id, titol, assignatura, "pendent", data_limit)
    tasques.append(tasca)
    desar_tasques(tasques)
    print(f"Tasca [ID: {tasca.id}] creada amb èxit")


def llistar_tasques():
    tasques = carregar_tasques()
    if not tasques:
        print("Registre de tasques buit.")
        return
    for tasca in tasques:
        print(f"[{tasca.id}] {tasca.titol} ({tasca.assignatura}) - estat: {tasca.estat}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Gestor de tasques acadèmiques.")
    subcomandes = parser.add_subparsers(dest="comanda", required=True)

    afegir = subcomandes.add_parser("add", help="Afegeix una nova tasca")
    afegir.add_argument("--title", required=True, help="Títol de la tasca")
    afegir.add_argument("--subject", required=True, help="Assignatura de la tasca")
    afegir.add_argument("--due", help="Data límit en format YYYY-MM-DD")

    subcomandes.add_parser("list", help="Mostra totes les tasques")

    args = parser.parse_args(argv)
    if args.comanda == "add":
        afegir_tasca(args.title, args.subject, args.due)
    elif args.comanda == "list":
        llistar_tasques()


if __name__ == "__main__":
    main()
