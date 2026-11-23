import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

CODI = Path(__file__).resolve().parent.parent / "src"


@pytest.fixture
def aplicacio(tmp_path):
    directori_codi = tmp_path / "src"
    directori_codi.mkdir()
    for nom in ("models.py", "tasks_app.py"):
        shutil.copy(CODI / nom, directori_codi / nom)
    fitxer = tmp_path / "data" / "tasks.json"
    fitxer.parent.mkdir()
    fitxer.write_text("[]\n", encoding="utf-8")
    return directori_codi / "tasks_app.py", fitxer


def executar(app, *args):
    return subprocess.run(
        [sys.executable, str(app), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_gs_01_creacio_correcta(aplicacio):
    app, fitxer = aplicacio

    resultat = executar(
        app,
        "add",
        "--title",
        "Pràctica 1",
        "--subject",
        "RS",
        "--due",
        "2026-12-01",
    )

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "Tasca [ID: 1] creada amb èxit"
    assert json.loads(fitxer.read_text(encoding="utf-8")) == [
        {
            "id": 1,
            "titol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "pendent",
            "data_limit": "2026-12-01",
        }
    ]


def test_gs_02_llistat_buit(aplicacio):
    app, _ = aplicacio

    resultat = executar(app, "list")

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "Registre de tasques buit."


def test_gs_03_llistat_amb_registres(aplicacio):
    app, fitxer = aplicacio
    fitxer.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "titol": "Pràctica 1",
                    "assignatura": "RS",
                    "estat": "pendent",
                },
                {
                    "id": 2,
                    "titol": "Examen parcial",
                    "assignatura": "SO",
                    "estat": "pendent",
                },
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    resultat = executar(app, "list")

    assert resultat.returncode == 0
    assert resultat.stdout.strip().splitlines() == [
        "[1] Pràctica 1 (RS) - estat: pendent",
        "[2] Examen parcial (SO) - estat: pendent",
    ]


def test_gs_04_crear_amb_data_limit(aplicacio):
    app, fitxer = aplicacio

    resultat = executar(
        app,
        "add",
        "--title",
        "Pràctica 2",
        "--subject",
        "RS",
        "--due",
        "2026-12-01",
    )

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "Tasca [ID: 1] creada amb èxit"
    primer_registre = json.loads(fitxer.read_text(encoding="utf-8"))
    assert primer_registre[0]["data_limit"] == "2026-12-01"
    assert primer_registre[0]["estat"] == "pendent"

    resultat = executar(app, "list")

    assert resultat.returncode == 0
    assert json.loads(fitxer.read_text(encoding="utf-8")) == primer_registre


@pytest.mark.parametrize(
    "data", ["2026-02-30", "01/12/2026", "text", "2026-1-1", "2026-13-01"]
)
def test_gs_05_rebutjar_dates_invalidades(aplicacio, data):
    app, fitxer = aplicacio
    original = fitxer.read_text(encoding="utf-8")

    resultat = executar(
        app, "add", "--title", "Prova", "--subject", "RS", "--due", data
    )

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "error: fecha invalida"
    assert fitxer.read_text(encoding="utf-8") == original


def test_gs_06_alta_sense_data(aplicacio):
    app, fitxer = aplicacio
    original = fitxer.read_text(encoding="utf-8")

    resultat = executar(app, "add", "--title", "Prova", "--subject", "RS")

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "error: fecha invalida"
    assert fitxer.read_text(encoding="utf-8") == original


def test_data_passada_valida(aplicacio):
    app, fitxer = aplicacio

    resultat = executar(
        app, "add", "--title", "Antiga", "--subject", "RS", "--due", "2020-01-01"
    )

    assert resultat.stdout.strip() == "Tasca [ID: 1] creada amb èxit"
    assert json.loads(fitxer.read_text(encoding="utf-8"))[0]["data_limit"] == "2020-01-01"


def test_id_automatic_segon_maxim_existent(aplicacio):
    app, fitxer = aplicacio
    fitxer.write_text(
        json.dumps(
            [
                {
                    "id": 5,
                    "titol": "Antiga",
                    "assignatura": "RS",
                    "estat": "pendent",
                }
            ]
        ),
        encoding="utf-8",
    )

    resultat = executar(
        app, "add", "--title", "Nova", "--subject", "SO", "--due", "2026-12-01"
    )

    assert resultat.stdout.strip() == "Tasca [ID: 6] creada amb èxit"
    ids = [tasca["id"] for tasca in json.loads(fitxer.read_text(encoding="utf-8"))]
    assert ids == [5, 6]


def test_gs_07_modificar_titol(aplicacio):
    app, fitxer = aplicacio
    registre = {
        "id": 1,
        "titol": "Pràctica 1",
        "assignatura": "RS",
        "estat": "pendent",
        "data_limit": "2026-12-01",
    }
    fitxer.write_text(json.dumps([registre], ensure_ascii=False), encoding="utf-8")

    resultat = executar(app, "setTitle", "--id", "1", "--title", "Títol revisat")

    assert resultat.returncode == 0
    desat = json.loads(fitxer.read_text(encoding="utf-8"))
    assert desat == [{**registre, "titol": "Títol revisat"}]

    resultat = executar(app, "list")

    assert resultat.returncode == 0
    assert json.loads(fitxer.read_text(encoding="utf-8")) == desat


def test_gs_12_set_title_id_inexistent(aplicacio):
    app, fitxer = aplicacio
    fitxer.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "titol": "Pràctica 1",
                    "assignatura": "RS",
                    "estat": "pendent",
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    original = fitxer.read_text(encoding="utf-8")

    resultat = executar(app, "setTitle", "--id", "999", "--title", "Nou títol")

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "error: id no encontrado"
    assert fitxer.read_text(encoding="utf-8") == original
