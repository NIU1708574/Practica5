# TASKS.md - Tasks_app

## Criteri de finalització

Una tasca es marca [x] quan la seva implementació i les comprovacions
associades són correctes. Les validacions globals comproven regressions;
no substitueixen les proves de cada funcionalitat.

## Increment 1: MVP - Creació i Llistat de Tasques

Objectiu: Tenir una versió CLI funcional per afegir i consultar tasques en JSON.

### Tasques d'Execució:

- [x] Tasca 1.1: Crear estructura de directoris (`src/`, `test/`, `data/`) i fitxer `data/tasks.json` inicial. (Requisits RF-01 i RF-02)
  Requisits: RF-01 i RF-02. Escenari: GS-31. Dependències: cap.

- [x] Tasca 1.2: Implementar model de dades `Task` a `src/models.py` amb mètodes de serialització JSON.
  Requisit: RF-01. Escenaris: GS-01 i GS-04 (persistència). Dependència: 1.1.

- [x] Tasca 1.3: Desenvolupar Tasks_app a `src/tasks_app.py` amb opcions `add` i `list`.(Requisits RF-03 i RF-04)
  Requisits: RF-01 a RF-04. Escenaris: GS-01, GS-02 i GS-03. Dependència: 1.2.

- [x] Tasca 1.4: Crear test d'integració a `test/test_tasks_app.py` segons els escenaris GS-01, GS-02 i GS-03.
  Requisits: RF-01 a RF-04. Escenaris: GS-01, GS-02 i GS-03. Dependència: 1.3.

- [x] Tasca 1.5: Validar execució amb OpenCode i verificar que tots els tests passen (`python3 -m pytest test`).
  Requisits: RF-01 a RF-04. Escenaris: GS-01, GS-02 i GS-03. Dependència: 1.4.

## Increment 2: Dates límit, modificacions i estats

Objectiu: ampliar l’aplicació mantenint les dades existents
i verificant cada funcionalitat abans de continuar.

### Model i creació

- [x] Tasca 2.1: Ampliar el model i la persistència amb data_limit.
  Admetre tasques antigues amb l’atribut absent o null.
  No assignar dates automàticament.
  Afegir proves de lectura, escriptura i compatibilitat.
  Requisits: RF-01, RF-15 i RF-20.
  Escenaris: GS-14.
  Dependència: 1.5.

- [x] Tasca 2.2: Ampliar add amb --due obligatori i validar dates.
  Mostrar el missatge especificat quan la data falta o és invàlida.
  Garantir IDs automàtics segons el màxim existent.
  Adaptar la prova de creació del primer increment.
  Afegir proves de dates vàlides, invàlides i absents.
  Requisits: RF-03, RF-05, RF-06 i RF-21.
  Escenaris: GS-01 adaptat, GS-04, GS-05 i GS-06.
  Dependència: 2.1.

### Modificació d’atributs

- [x] Tasca 2.3: Implementar setTitle i les proves corresponents.
  Verificar ID inexistent, persistència i conservació dels altres atributs.
  Requisits: RF-07, RF-11 i RF-20.
  Escenaris: GS-07 i GS-12 per a setTitle.
  Dependència: 2.2.

- [x] Tasca 2.4: Implementar setSubject i les proves corresponents.
  Verificar ID inexistent, persistència i conservació dels altres atributs.
  Requisits: RF-08, RF-11 i RF-20.
  Escenaris: GS-08 i GS-12 per a setSubject.
  Dependència: 2.3.

- [x] Tasca 2.5: Implementar setDueDate i les proves corresponents.
  Permetre assignar dates a tasques antigues.
  Verificar dates invàlides, ID inexistent i persistència.
  Requisits: RF-06, RF-09, RF-11 i RF-20.
  Escenaris: GS-09, GS-10 i GS-12 per a setDueDate.
  Dependència: 2.4.

- [x] Tasca 2.6: Implementar setId i les proves corresponents.
  Verificar ID inexistent, duplicat, invàlid i igual a l’actual.
  Comprovar la creació de tasques després de canviar un ID.
  Requisits: RF-11, RF-16, RF-17, RF-18, RF-20 i RF-21.
  Escenaris: GS-12 per a setId, GS-16, GS-17, GS-18,
  GS-20 i GS-21.a.
  Dependència: 2.5.

### Canvis d’estat

- [x] Tasca 2.7: Implementar completeTask i les proves corresponents.
  Verificar ID inexistent, persistència i repetició del comandament.
  Requisits: RF-10, RF-11 i RF-20.
  Escenaris: GS-11, GS-12 per a completeTask
  i GS-21.b.
  Dependència: 2.6.

- [x] Tasca 2.8: Implementar markPending i les proves de canvi d’estat.
  Verificar ID inexistent, persistència i repetició del comandament.
  La comprovació dels avisos de GS-19 es farà a la tasca 2.9.
  Requisits: RF-11, RF-19 i RF-20.
  Escenaris: canvi d’estat de GS-19, GS-12 per a markPending
  i GS-21.c.
  Dependència: 2.7.

### Llistat i validació

- [x] Tasca 2.9: Ampliar list amb la data límit i els avisos.
  Mostrar "sense data" per a les tasques que no en tenen.
  Calcular els avisos segons la data local actual.
  Utilitzar una data controlada en les proves.
  Comprovar els límits d’avui, ahir, sis dies i set dies.
  Adaptar les proves del llistat del primer increment.
  Requisits: RF-04, RF-12, RF-13, RF-14 i RF-22.
  Escenaris: GS-02, GS-03 adaptat, GS-13, GS-14, GS-15
  i comprovació completa de GS-19.
  Dependència: 2.8.

- [x] Tasca 2.10: Validar el segon increment complet.
  Executar python3 -m pytest test.
  Verificar la creació de data/tasks.json quan no existeix.
  Comprovar manualment tots els comandaments.
  Comprovar que els errors no modifiquen el registre.
  Confirmar la persistència entre execucions.
  Requisits: RF-01 a RF-22 amb les ampliacions de v2.0.
  Escenaris: GS-01 a GS-21 i GS-31, amb les adaptacions documentades.
  Dependència: 2.9.

## Increment 3: Resums i filtres

Objectiu: facilitar la consulta del registre sense modificar les dades.

- [x] Tasca 3.1: Implementar list --summary amb els cinc recomptes.
  Reutilitzar les regles d’urgència i caducitat del segon increment.
  Afegir proves amb una data de referència controlada.
  Verificar el resum d’un registre buit.
  Requisits: RF-23, RF-24, RF-30 i RF-31.
  Escenaris: GS-22, GS-29 i GS-30.
  Dependència: 2.10.

- [x] Tasca 3.2: Implementar list --subject.
  Comparar l’assignatura completa ignorant majúscules i minúscules.
  Permetre combinar el filtre amb --summary.
  Afegir proves amb coincidències i sense coincidències.
  Requisits: RF-25, RF-28, RF-29, RF-30 i RF-31.
  Escenaris: GS-23, GS-26, GS-27, GS-28 i GS-29.
  Dependència: 3.1.

- [x] Tasca 3.3: Implementar list --keyword i la combinació de filtres.
  Cercar el text dins del títol ignorant majúscules i minúscules.
  Aplicar tots els filtres abans de calcular el resum.
  Afegir proves de cerca, combinació i resum amb els dos filtres.
  Requisits: RF-26, RF-27, RF-28, RF-29, RF-30 i RF-31.
  Escenaris: GS-24, GS-25 i GS-29.
  Ampliar GS-26 i GS-28 amb el filtre de títol.
  Dependència: 3.2.

- [x] Tasca 3.4: Validar el tercer increment complet.
  Executar python3 -m pytest test.
  Comprovar manualment els nous comandaments.
  Verificar que list sense opcions conserva el comportament anterior.
  Comprovar que les funcionalitats dels increments anteriors funcionen.
  Requisits: RF-01 a RF-31 amb les ampliacions vigents.
  Escenaris: GS-01 a GS-31, amb les adaptacions vigents i els subescenaris de GS-21.
  Dependència: 3.3.


## Revisió final de la documentació

- [x] Tasca R.1: Precisar els requisits, els escenaris i la traçabilitat.
  Identificar GS-31 per a la prova existent de RF-02.
  Mantenir les funcionalitats i els identificadors dels requisits existents.
  Completar la prova del resum filtrat només pel títol (GS-26).
  Requisits: RF-01 a RF-31.
  Escenaris: GS-01 a GS-31 amb les adaptacions vigents.
  Dependència: 3.4.
  Validació: suite completa de proves i revisió de les referències.

Les dependències indiquen l’ordre de treball adoptat. Les tasques 2.6,
2.7 i 2.8 tenen implementacions diferenciades, però es van registrar
juntes al commit 8eda928. Es conserva l’historial original.
