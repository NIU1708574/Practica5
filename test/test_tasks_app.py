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

    resultat = executar(app, "add", "--title", "Pràctica 1", "--subject", "RS")

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "Tasca [ID: 1] creada amb èxit"
    assert json.loads(fitxer.read_text(encoding="utf-8")) == [
        {
            "id": 1,
            "titol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "pendent",
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
