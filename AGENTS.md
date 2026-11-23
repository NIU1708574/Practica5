# AGENTS.md — Directives per a OpenCode

## Entorn i stack tècnic
- Llenguatge: Python 3.11+.
- Interfície: línia de comandes amb argparse o cmd.
- Persistència: fitxer JSON local data/tasks.json.
- Entorn d’execució: contenidor Docker de la pràctica.

## Comandes de desenvolupament
- Consultar ajuda: python3 src/tasks_app.py --help
- Executar aplicació: python3 src/tasks_app.py <comandament>
- Executar tots els tests: python3 -m pytest test
- Executar tests d’integració: python3 -m pytest test/test_tasks_app.py

## Convencions de codi
- Seguir PEP8.
- Escriure el codi i els comentaris en català.
- Respectar els noms dels comandaments i els missatges literals de SPECIFICATIONS.md.
- Mantenir la separació entre model de dades, persistència i interfície CLI.

## Font de veritat
- SPECIFICATIONS.md defineix el comportament requerit.
- TASKS.md defineix les tasques i l’ordre d’execució.
- No inventar funcionalitats ni modificar requisits per adaptar-los al codi.
- Si hi ha contradiccions que impedeixen executar una tasca, explicar-les abans de continuar.

## Gestió de tasques
1. Llegir AGENTS.md, SPECIFICATIONS.md i TASKS.md.
2. Identificar la primera tasca pendent [ ].
3. Marcar-la com a [/] abans de començar.
4. Executar únicament una tasca per torn.
5. Verificar els requisits i escenaris associats a la tasca.
6. Executar les proves aplicables i comprovar possibles regressions.
7. Marcar-la com a [x] només quan estigui completada i verificada.
8. Mostrar els canvis i els resultats de les comprovacions.
9. Aturar-se i esperar confirmació abans de començar la següent tasca.

## Persistència i dates
- Conservar les tasques del primer increment que no tenen data límit.
- No assignar dates automàticament a les tasques antigues.
- Les operacions rebutjades no han de modificar les dades.
- Utilitzar la data local del sistema per calcular els avisos.
- Les proves han de controlar la data de referència per ser reproduïbles.
- Les proves han d’utilitzar dades temporals i no alterar data/tasks.json.

## Límits
- No instal·lar dependències externes sense autorització.
- No modificar la configuració del contenidor sense autorització.
- Limitar els canvis als fitxers del projecte.
- Actualitzar TASKS.md per reflectir el progrés.
- No modificar SPECIFICATIONS.md ni AGENTS.md sense una petició explícita.
- No fer commits ni push sense una petició explícita de l’usuari.