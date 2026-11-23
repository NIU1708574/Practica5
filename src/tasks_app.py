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


def buscar_tasca(tasques, id_valor):
    try:
        identificador = int(id_valor)
    except (TypeError, ValueError):
        return None
    for tasca in tasques:
        if tasca.id == identificador:
            return tasca
    return None


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


def modificar_titol(id_valor, titol):
    tasques = carregar_tasques()
    tasca = buscar_tasca(tasques, id_valor)
    if tasca is None:
        print("error: id no encontrado")
        return
    tasca.titol = titol
    desar_tasques(tasques)


def modificar_assignatura(id_valor, assignatura):
    tasques = carregar_tasques()
    tasca = buscar_tasca(tasques, id_valor)
    if tasca is None:
        print("error: id no encontrado")
        return
    tasca.assignatura = assignatura
    desar_tasques(tasques)


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

    canviar_titol = subcomandes.add_parser(
        "setTitle", help="Canvia el títol d'una tasca"
    )
    canviar_titol.add_argument("--id", required=True, help="ID de la tasca")
    canviar_titol.add_argument("--title", required=True, help="Nou títol de la tasca")

    canviar_assignatura = subcomandes.add_parser(
        "setSubject", help="Canvia l'assignatura d'una tasca"
    )
    canviar_assignatura.add_argument("--id", required=True, help="ID de la tasca")
    canviar_assignatura.add_argument(
        "--subject", required=True, help="Nova assignatura de la tasca"
    )

    args = parser.parse_args(argv)
    if args.comanda == "add":
        afegir_tasca(args.title, args.subject, args.due)
    elif args.comanda == "list":
        llistar_tasques()
    elif args.comanda == "setTitle":
        modificar_titol(args.id, args.title)
    elif args.comanda == "setSubject":
        modificar_assignatura(args.id, args.subject)


if __name__ == "__main__":
    main()
