import json
from pathlib import Path

import pytest

ARREL = Path(__file__).resolve().parent.parent


@pytest.fixture
def moduls(monkeypatch):
    monkeypatch.syspath_prepend(str(ARREL / "src"))
    import models
    import tasks_app

    return models.Task, tasks_app


def escriure_registre(fitxer, registres):
    fitxer.write_text(json.dumps(registres, ensure_ascii=False), encoding="utf-8")


def test_lectura_tasca_antiga_sense_atribut(moduls, monkeypatch, tmp_path):
    Task, tasks_app = moduls
    fitxer = tmp_path / "tasks.json"
    escriure_registre(
        fitxer,
        [
            {
                "id": 1,
                "titol": "Pràctica antiga",
                "assignatura": "RS",
                "estat": "pendent",
            }
        ],
    )
    monkeypatch.setattr(tasks_app, "fitxer_tasques", lambda: fitxer)

    tasques = tasks_app.carregar_tasques()

    assert len(tasques) == 1
    assert isinstance(tasques[0], Task)
    assert tasques[0].id == 1
    assert tasques[0].titol == "Pràctica antiga"
    assert tasques[0].data_limit is None


def test_lectura_tasca_antiga_amb_data_limit_null(moduls, monkeypatch, tmp_path):
    _, tasks_app = moduls
    fitxer = tmp_path / "tasks.json"
    escriure_registre(
        fitxer,
        [
            {
                "id": 2,
                "titol": "Examen antic",
                "assignatura": "SO",
                "estat": "completada",
                "data_limit": None,
            }
        ],
    )
    monkeypatch.setattr(tasks_app, "fitxer_tasques", lambda: fitxer)

    tasques = tasks_app.carregar_tasques()

    assert tasques[0].data_limit is None
    assert tasques[0].estat == "completada"


def test_escriptura_amb_data_limit(moduls, monkeypatch, tmp_path):
    Task, tasks_app = moduls
    fitxer = tmp_path / "subdirectori" / "tasks.json"
    monkeypatch.setattr(tasks_app, "fitxer_tasques", lambda: fitxer)
    tasca = Task(3, "Pràctica nova", "RS", "pendent", "2026-12-01")

    tasks_app.desar_tasques([tasca])

    desat = json.loads(fitxer.read_text(encoding="utf-8"))
    assert desat == [
        {
            "id": 3,
            "titol": "Pràctica nova",
            "assignatura": "RS",
            "estat": "pendent",
            "data_limit": "2026-12-01",
        }
    ]
    assert tasks_app.carregar_tasques() == [tasca]


def test_compatibilitat_no_assigna_data_automatica(moduls, monkeypatch, tmp_path):
    _, tasks_app = moduls
    fitxer = tmp_path / "tasks.json"
    registre = {
        "id": 1,
        "titol": "Tasca antiga",
        "assignatura": "RS",
        "estat": "pendent",
    }
    escriure_registre(fitxer, [registre])
    monkeypatch.setattr(tasks_app, "fitxer_tasques", lambda: fitxer)

    tasques = tasks_app.carregar_tasques()
    tasks_app.desar_tasques(tasques)

    desat = json.loads(fitxer.read_text(encoding="utf-8"))
    assert "data_limit" not in desat[0]
    assert tasks_app.carregar_tasques()[0].data_limit is None


def test_serialitzacio_json_amb_data_limit(moduls):
    Task, _ = moduls
    tasca = Task(1, "Prova", "SO", "pendent", "2026-11-30")

    text = tasca.to_json()

    assert json.loads(text)["data_limit"] == "2026-11-30"
    assert Task.from_json(text) == tasca
