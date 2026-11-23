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

    runner = tmp_path / "executar.py"
    runner.write_text(
        "import sys\n"
        "from datetime import date\n"
        "from pathlib import Path\n"
        "sys.path.insert(0, str(Path(__file__).parent / 'src'))\n"
        "import tasks_app\n"
        "referencia = sys.argv[1]\n"
        "if referencia:\n"
        "    any, mes, dia = (int(part) for part in referencia.split('-'))\n"
        "    class DataControlada(date):\n"
        "        @classmethod\n"
        "        def today(cls):\n"
        "            return cls(any, mes, dia)\n"
        "    tasks_app.date = DataControlada\n"
        "tasks_app.main(sys.argv[2:])\n",
        encoding="utf-8",
    )
    return directori_codi / "tasks_app.py", fitxer


def executar(app, *args, avui=None):
    if avui is None:
        comanda = [sys.executable, str(app), *args]
    else:
        runner = app.parent.parent / "executar.py"
        comanda = [sys.executable, str(runner), avui, *args]
    return subprocess.run(
        comanda,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture
def registre_comu(aplicacio):
    app, fitxer = aplicacio
    fitxer.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "titol": "Pràctica requisits",
                    "assignatura": "RS",
                    "estat": "pendent",
                    "data_limit": "2026-11-22",
                },
                {
                    "id": 2,
                    "titol": "Examen parcial",
                    "assignatura": "RS",
                    "estat": "pendent",
                    "data_limit": "2026-11-23",
                },
                {
                    "id": 3,
                    "titol": "Pràctica processos",
                    "assignatura": "SO",
                    "estat": "completada",
                    "data_limit": "2026-11-20",
                },
                {
                    "id": 4,
                    "titol": "Lectura tema 4",
                    "assignatura": "SO",
                    "estat": "pendent",
                    "data_limit": "2026-12-10",
                },
                {
                    "id": 5,
                    "titol": "Revisió apunts",
                    "assignatura": "RS",
                    "estat": "pendent",
                    "data_limit": None,
                },
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return app, fitxer


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
        "[1] Pràctica 1 (RS) - estat: pendent - data límit: sense data",
        "[2] Examen parcial (SO) - estat: pendent - data límit: sense data",
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


def test_gs_08_modificar_assignatura(aplicacio):
    app, fitxer = aplicacio
    registre = {
        "id": 1,
        "titol": "Pràctica 1",
        "assignatura": "RS",
        "estat": "pendent",
        "data_limit": "2026-12-01",
    }
    fitxer.write_text(json.dumps([registre], ensure_ascii=False), encoding="utf-8")

    resultat = executar(app, "setSubject", "--id", "1", "--subject", "SO")

    assert resultat.returncode == 0
    desat = json.loads(fitxer.read_text(encoding="utf-8"))
    assert desat == [{**registre, "assignatura": "SO"}]

    resultat = executar(app, "list")

    assert resultat.returncode == 0
    assert json.loads(fitxer.read_text(encoding="utf-8")) == desat


def test_gs_12_set_subject_id_inexistent(aplicacio):
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

    resultat = executar(app, "setSubject", "--id", "999", "--subject", "SO")

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "error: id no encontrado"
    assert fitxer.read_text(encoding="utf-8") == original


def test_gs_09_assignar_data_a_tasca_antiga(aplicacio):
    app, fitxer = aplicacio
    registre = {
        "id": 1,
        "titol": "Tasca antiga",
        "assignatura": "RS",
        "estat": "pendent",
    }
    fitxer.write_text(json.dumps([registre], ensure_ascii=False), encoding="utf-8")

    resultat = executar(app, "setDueDate", "--id", "1", "--due", "2026-12-03")

    assert resultat.returncode == 0
    desat = json.loads(fitxer.read_text(encoding="utf-8"))
    assert desat == [{**registre, "data_limit": "2026-12-03"}]

    resultat = executar(app, "list")

    assert resultat.returncode == 0
    assert json.loads(fitxer.read_text(encoding="utf-8")) == desat


def test_gs_09_modificar_data_existent(aplicacio):
    app, fitxer = aplicacio
    registre = {
        "id": 1,
        "titol": "Pràctica 1",
        "assignatura": "RS",
        "estat": "pendent",
        "data_limit": "2026-12-01",
    }
    fitxer.write_text(json.dumps([registre], ensure_ascii=False), encoding="utf-8")

    resultat = executar(app, "setDueDate", "--id", "1", "--due", "2026-12-03")

    assert resultat.returncode == 0
    assert json.loads(fitxer.read_text(encoding="utf-8")) == [
        {**registre, "data_limit": "2026-12-03"}
    ]


@pytest.mark.parametrize("data", ["2026-02-30", "01/12/2026", "text"])
def test_gs_10_data_invalida_no_modifica(aplicacio, data):
    app, fitxer = aplicacio
    fitxer.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "titol": "Pràctica 1",
                    "assignatura": "RS",
                    "estat": "pendent",
                    "data_limit": "2026-12-01",
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    original = fitxer.read_text(encoding="utf-8")

    resultat = executar(app, "setDueDate", "--id", "1", "--due", data)

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "error: fecha invalida"
    assert fitxer.read_text(encoding="utf-8") == original


def test_gs_10_sense_data_no_modifica(aplicacio):
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

    resultat = executar(app, "setDueDate", "--id", "1")

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "error: fecha invalida"
    assert fitxer.read_text(encoding="utf-8") == original


def test_gs_12_set_due_date_id_inexistent(aplicacio):
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

    resultat = executar(app, "setDueDate", "--id", "999", "--due", "2026-12-03")

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "error: id no encontrado"
    assert fitxer.read_text(encoding="utf-8") == original


def test_gs_16_canviar_id(aplicacio):
    app, fitxer = aplicacio
    registre = {
        "id": 1,
        "titol": "Pràctica 1",
        "assignatura": "RS",
        "estat": "pendent",
        "data_limit": "2026-12-01",
    }
    fitxer.write_text(json.dumps([registre], ensure_ascii=False), encoding="utf-8")

    resultat = executar(app, "setId", "--id", "1", "--newId", "5")

    assert resultat.returncode == 0
    desat = json.loads(fitxer.read_text(encoding="utf-8"))
    assert desat == [{**registre, "id": 5}]

    resultat = executar(app, "list")

    assert resultat.returncode == 0
    assert json.loads(fitxer.read_text(encoding="utf-8")) == desat


def test_gs_12_set_id_inexistent(aplicacio):
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

    resultat = executar(app, "setId", "--id", "999", "--newId", "5")

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "error: id no encontrado"
    assert fitxer.read_text(encoding="utf-8") == original


def test_gs_17_rebutjar_id_duplicat(aplicacio):
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
                    "id": 5,
                    "titol": "Pràctica 2",
                    "assignatura": "SO",
                    "estat": "pendent",
                },
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    original = fitxer.read_text(encoding="utf-8")

    resultat = executar(app, "setId", "--id", "1", "--newId", "5")

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "error: id ya existente"
    assert fitxer.read_text(encoding="utf-8") == original


@pytest.mark.parametrize("nou_id", ["0", "-2", "abc", "1.5"])
def test_gs_18_rebutjar_id_invalid(aplicacio, nou_id):
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

    resultat = executar(app, "setId", "--id", "1", "--newId", nou_id)

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "error: id invalido"
    assert fitxer.read_text(encoding="utf-8") == original


def test_gs_20_crear_despres_canvi_id(aplicacio):
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

    resultat = executar(app, "setId", "--id", "1", "--newId", "5")
    assert resultat.returncode == 0

    resultat = executar(
        app, "add", "--title", "Pràctica 2", "--subject", "SO", "--due", "2026-12-01"
    )

    assert resultat.stdout.strip() == "Tasca [ID: 6] creada amb èxit"
    ids = [tasca["id"] for tasca in json.loads(fitxer.read_text(encoding="utf-8"))]
    assert ids == [5, 6]


def test_gs_21_set_id_igual_no_canvia_res(aplicacio):
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

    resultat = executar(app, "setId", "--id", "1", "--newId", "1")

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == ""
    assert fitxer.read_text(encoding="utf-8") == original


def test_gs_11_completar_tasca(aplicacio):
    app, fitxer = aplicacio
    registre = {
        "id": 1,
        "titol": "Pràctica 1",
        "assignatura": "RS",
        "estat": "pendent",
        "data_limit": "2026-12-01",
    }
    fitxer.write_text(json.dumps([registre], ensure_ascii=False), encoding="utf-8")

    resultat = executar(app, "completeTask", "--id", "1")

    assert resultat.returncode == 0
    desat = json.loads(fitxer.read_text(encoding="utf-8"))
    assert desat == [{**registre, "estat": "completada"}]

    resultat = executar(app, "list")

    assert resultat.returncode == 0
    assert json.loads(fitxer.read_text(encoding="utf-8")) == desat


def test_gs_12_complete_task_id_inexistent(aplicacio):
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

    resultat = executar(app, "completeTask", "--id", "999")

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "error: id no encontrado"
    assert fitxer.read_text(encoding="utf-8") == original


def test_gs_21_completar_dues_vegades(aplicacio):
    app, fitxer = aplicacio
    registre = {
        "id": 1,
        "titol": "Pràctica 1",
        "assignatura": "RS",
        "estat": "pendent",
        "data_limit": "2026-12-01",
    }
    fitxer.write_text(json.dumps([registre], ensure_ascii=False), encoding="utf-8")

    primer = executar(app, "completeTask", "--id", "1")
    desat = fitxer.read_text(encoding="utf-8")
    segon = executar(app, "completeTask", "--id", "1")

    assert primer.returncode == 0
    assert primer.stdout.strip() == ""
    assert segon.returncode == 0
    assert segon.stdout.strip() == ""
    assert fitxer.read_text(encoding="utf-8") == desat
    assert json.loads(desat) == [{**registre, "estat": "completada"}]


def test_gs_19_retornar_a_pendent(aplicacio):
    app, fitxer = aplicacio
    registre = {
        "id": 5,
        "titol": "Pràctica 1",
        "assignatura": "RS",
        "estat": "completada",
        "data_limit": "2026-11-22",
    }
    fitxer.write_text(json.dumps([registre], ensure_ascii=False), encoding="utf-8")

    resultat = executar(app, "markPending", "--id", "5")

    assert resultat.returncode == 0
    desat = json.loads(fitxer.read_text(encoding="utf-8"))
    assert desat == [{**registre, "estat": "pendent"}]

    resultat = executar(app, "list")

    assert resultat.returncode == 0
    assert json.loads(fitxer.read_text(encoding="utf-8")) == desat


def test_gs_12_mark_pending_id_inexistent(aplicacio):
    app, fitxer = aplicacio
    fitxer.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "titol": "Pràctica 1",
                    "assignatura": "RS",
                    "estat": "completada",
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    original = fitxer.read_text(encoding="utf-8")

    resultat = executar(app, "markPending", "--id", "999")

    assert resultat.returncode == 0
    assert resultat.stdout.strip() == "error: id no encontrado"
    assert fitxer.read_text(encoding="utf-8") == original


def test_gs_21_mark_pending_dues_vegades(aplicacio):
    app, fitxer = aplicacio
    registre = {
        "id": 1,
        "titol": "Pràctica 1",
        "assignatura": "RS",
        "estat": "pendent",
        "data_limit": "2026-12-01",
    }
    fitxer.write_text(json.dumps([registre], ensure_ascii=False), encoding="utf-8")
    original = fitxer.read_text(encoding="utf-8")

    primer = executar(app, "markPending", "--id", "1")
    segon = executar(app, "markPending", "--id", "1")

    assert primer.returncode == 0
    assert primer.stdout.strip() == ""
    assert segon.returncode == 0
    assert segon.stdout.strip() == ""
    assert fitxer.read_text(encoding="utf-8") == original
    assert json.loads(original) == [registre]


@pytest.mark.parametrize(
    ("data_limit", "avis"),
    [
        ("2026-11-22", "[CADUCADA]"),
        ("2026-11-23", "[URGENT]"),
        ("2026-11-29", "[URGENT]"),
        ("2026-11-30", ""),
    ],
)
def test_gs_13_avisos_segons_data(aplicacio, data_limit, avis):
    app, fitxer = aplicacio
    fitxer.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "titol": "Pràctica 1",
                    "assignatura": "RS",
                    "estat": "pendent",
                    "data_limit": data_limit,
                }
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    original = fitxer.read_text(encoding="utf-8")

    resultat = executar(app, "list", avui="2026-11-23")

    sufix = f" {avis}" if avis else ""
    assert resultat.returncode == 0
    assert resultat.stdout.strip() == (
        f"[1] Pràctica 1 (RS) - estat: pendent"
        f" - data límit: {data_limit}{sufix}"
    )
    assert fitxer.read_text(encoding="utf-8") == original


def test_gs_14_tasques_antigues_sense_data(aplicacio):
    app, fitxer = aplicacio
    fitxer.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "titol": "Sense clau",
                    "assignatura": "RS",
                    "estat": "pendent",
                },
                {
                    "id": 2,
                    "titol": "Amb null",
                    "assignatura": "SO",
                    "estat": "pendent",
                    "data_limit": None,
                },
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    original = fitxer.read_text(encoding="utf-8")

    resultat = executar(app, "list", avui="2026-11-23")

    assert resultat.returncode == 0
    assert resultat.stdout.strip().splitlines() == [
        "[1] Sense clau (RS) - estat: pendent - data límit: sense data",
        "[2] Amb null (SO) - estat: pendent - data límit: sense data",
    ]
    assert fitxer.read_text(encoding="utf-8") == original


def test_gs_15_completades_sense_avisos(aplicacio):
    app, fitxer = aplicacio
    fitxer.write_text(
        json.dumps(
            [
                {
                    "id": indice,
                    "titol": f"Tasca {indice}",
                    "assignatura": "RS",
                    "estat": "completada",
                    "data_limit": data_limit,
                }
                for indice, data_limit in enumerate(
                    ["2026-11-22", "2026-11-23", "2026-11-29"], start=1
                )
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    resultat = executar(app, "list", avui="2026-11-23")

    llistat = resultat.stdout.strip().splitlines()
    assert resultat.returncode == 0
    assert llistat == [
        "[1] Tasca 1 (RS) - estat: completada - data límit: 2026-11-22",
        "[2] Tasca 2 (RS) - estat: completada - data límit: 2026-11-23",
        "[3] Tasca 3 (RS) - estat: completada - data límit: 2026-11-29",
    ]
    assert all(
        "[URGENT]" not in linia and "[CADUCADA]" not in linia for linia in llistat
    )


@pytest.mark.parametrize(
    ("data_limit", "avis"),
    [
        ("2026-11-22", "[CADUCADA]"),
        ("2026-11-23", "[URGENT]"),
        (None, ""),
    ],
)
def test_gs_19_avisos_despres_mark_pending(aplicacio, data_limit, avis):
    app, fitxer = aplicacio
    registre = {
        "id": 5,
        "titol": "Pràctica 1",
        "assignatura": "RS",
        "estat": "completada",
    }
    if data_limit is not None:
        registre["data_limit"] = data_limit
    fitxer.write_text(json.dumps([registre], ensure_ascii=False), encoding="utf-8")

    resultat = executar(app, "markPending", "--id", "5")
    assert resultat.returncode == 0

    resultat = executar(app, "list", avui="2026-11-23")

    data_mostrada = data_limit if data_limit is not None else "sense data"
    sufix = f" {avis}" if avis else ""
    assert resultat.returncode == 0
    assert resultat.stdout.strip() == (
        f"[5] Pràctica 1 (RS) - estat: pendent"
        f" - data límit: {data_mostrada}{sufix}"
    )


def test_gs_22_resum_general(registre_comu):
    app, _ = registre_comu

    resultat = executar(app, "list", "--summary", avui="2026-11-23")

    assert resultat.returncode == 0
    assert resultat.stdout.strip().splitlines() == [
        "Total: 5",
        "Pendents: 4",
        "Completades: 1",
        "Caducades: 1",
        "Urgents: 1",
    ]
    assert "Pràctica requisits" not in resultat.stdout


def test_gs_30_resum_registre_buit(aplicacio):
    app, _ = aplicacio

    resultat = executar(app, "list", "--summary", avui="2026-11-23")

    assert resultat.returncode == 0
    assert resultat.stdout.strip().splitlines() == [
        "Total: 0",
        "Pendents: 0",
        "Completades: 0",
        "Caducades: 0",
        "Urgents: 0",
    ]


def test_gs_29_consultes_no_modifiquen_dades(registre_comu):
    app, fitxer = registre_comu
    original = fitxer.read_text(encoding="utf-8")

    resultat = executar(app, "list", "--summary", avui="2026-11-23")
    assert resultat.returncode == 0
    assert fitxer.read_text(encoding="utf-8") == original

    resultat = executar(app, "list", avui="2026-11-23")
    assert resultat.returncode == 0
    assert fitxer.read_text(encoding="utf-8") == original
