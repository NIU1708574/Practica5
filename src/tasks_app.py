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


def modificar_data_limit(id_valor, data_limit):
    tasques = carregar_tasques()
    tasca = buscar_tasca(tasques, id_valor)
    if tasca is None:
        print("error: id no encontrado")
        return
    if not es_data_valida(data_limit):
        print("error: fecha invalida")
        return
    tasca.data_limit = data_limit
    desar_tasques(tasques)


def canviar_identificador(id_valor, nou_id_valor):
    tasques = carregar_tasques()
    tasca = buscar_tasca(tasques, id_valor)
    if tasca is None:
        print("error: id no encontrado")
        return

    try:
        nou_id = int(nou_id_valor)
    except (TypeError, ValueError):
        print("error: id invalido")
        return
    if nou_id <= 0:
        print("error: id invalido")
        return
    if any(altre.id == nou_id for altre in tasques if altre is not tasca):
        print("error: id ya existente")
        return
    if tasca.id == nou_id:
        return

    tasca.id = nou_id
    desar_tasques(tasques)


def completar_tasca(id_valor):
    tasques = carregar_tasques()
    tasca = buscar_tasca(tasques, id_valor)
    if tasca is None:
        print("error: id no encontrado")
        return
    if tasca.estat == "completada":
        return
    tasca.estat = "completada"
    desar_tasques(tasques)


def retornar_a_pendent(id_valor):
    tasques = carregar_tasques()
    tasca = buscar_tasca(tasques, id_valor)
    if tasca is None:
        print("error: id no encontrado")
        return
    if tasca.estat == "pendent":
        return
    tasca.estat = "pendent"
    desar_tasques(tasques)


def avis_tasca(tasca, avui):
    if tasca.estat != "pendent" or not tasca.data_limit:
        return ""
    try:
        data_limit = date.fromisoformat(tasca.data_limit)
    except (TypeError, ValueError):
        return ""
    dies = (data_limit - avui).days
    if dies < 0:
        return "[CADUCADA]"
    if dies <= 6:
        return "[URGENT]"
    return ""


def recomptar_tasques(tasques):
    avui = date.today()
    recomptes = {
        "total": len(tasques),
        "pendents": 0,
        "completades": 0,
        "caducades": 0,
        "urgents": 0,
    }
    for tasca in tasques:
        if tasca.estat == "pendent":
            recomptes["pendents"] += 1
        elif tasca.estat == "completada":
            recomptes["completades"] += 1
        avis = avis_tasca(tasca, avui)
        if avis == "[CADUCADA]":
            recomptes["caducades"] += 1
        elif avis == "[URGENT]":
            recomptes["urgents"] += 1
    return recomptes


def mostrar_resum(tasques):
    recomptes = recomptar_tasques(tasques)
    print(f"Total: {recomptes['total']}")
    print(f"Pendents: {recomptes['pendents']}")
    print(f"Completades: {recomptes['completades']}")
    print(f"Caducades: {recomptes['caducades']}")
    print(f"Urgents: {recomptes['urgents']}")


def llistar_tasques(resum=False):
    tasques = carregar_tasques()
    if resum:
        mostrar_resum(tasques)
        return
    if not tasques:
        print("Registre de tasques buit.")
        return
    avui = date.today()
    for tasca in tasques:
        data_mostrada = tasca.data_limit if tasca.data_limit else "sense data"
        avis = avis_tasca(tasca, avui)
        sufix = f" {avis}" if avis else ""
        print(
            f"[{tasca.id}] {tasca.titol} ({tasca.assignatura})"
            f" - estat: {tasca.estat} - data límit: {data_mostrada}{sufix}"
        )


def main(argv=None):
    parser = argparse.ArgumentParser(description="Gestor de tasques acadèmiques.")
    subcomandes = parser.add_subparsers(dest="comanda", required=True)

    afegir = subcomandes.add_parser("add", help="Afegeix una nova tasca")
    afegir.add_argument("--title", required=True, help="Títol de la tasca")
    afegir.add_argument("--subject", required=True, help="Assignatura de la tasca")
    afegir.add_argument("--due", help="Data límit en format YYYY-MM-DD")

    llistat = subcomandes.add_parser("list", help="Mostra totes les tasques")
    llistat.add_argument(
        "--summary", action="store_true", help="Mostra únicament els recomptes"
    )

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

    canviar_data = subcomandes.add_parser(
        "setDueDate", help="Assigna o canvia la data límit d'una tasca"
    )
    canviar_data.add_argument("--id", required=True, help="ID de la tasca")
    canviar_data.add_argument("--due", help="Nova data límit en format YYYY-MM-DD")

    canviar_identificador_parser = subcomandes.add_parser(
        "setId", help="Canvia l'identificador d'una tasca"
    )
    canviar_identificador_parser.add_argument(
        "--id", required=True, help="ID actual de la tasca"
    )
    canviar_identificador_parser.add_argument(
        "--newId", required=True, help="Nou ID de la tasca"
    )

    completar = subcomandes.add_parser(
        "completeTask", help="Marca una tasca com a completada"
    )
    completar.add_argument("--id", required=True, help="ID de la tasca")

    marcar_pendent = subcomandes.add_parser(
        "markPending", help="Retorna una tasca a l'estat pendent"
    )
    marcar_pendent.add_argument("--id", required=True, help="ID de la tasca")

    args = parser.parse_args(argv)
    if args.comanda == "add":
        afegir_tasca(args.title, args.subject, args.due)
    elif args.comanda == "list":
        llistar_tasques(args.summary)
    elif args.comanda == "setTitle":
        modificar_titol(args.id, args.title)
    elif args.comanda == "setSubject":
        modificar_assignatura(args.id, args.subject)
    elif args.comanda == "setDueDate":
        modificar_data_limit(args.id, args.due)
    elif args.comanda == "setId":
        canviar_identificador(args.id, args.newId)
    elif args.comanda == "completeTask":
        completar_tasca(args.id)
    elif args.comanda == "markPending":
        retornar_a_pendent(args.id)


if __name__ == "__main__":
    main()
