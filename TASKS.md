# TASKS.md - Tasks\_app



## Increment 1: MVP - Creació i Llistat de Tasques

Objectiu: Tenir una versió CLI funcional per afegir i consultar tasques en JSON.



### Tasques d'Execució:

- [x] Tasca 1.1: Crear estructura de directoris (`src/`, `test/`, `data/`) i fitxer `data/tasks.json` inicial. (Requisits RF-01 i RF-02) 

- [x] Tasca 1.2: Implementar model de dades `Task` a `src/models.py` amb mètodes de serialització JSON.

- [x] Tasca 1.3: Desenvolupar Tasks\_app a `src/tasks\_app.py` amb opcions `add` i `list`.(Requisits RF-03 i RF-04)

- [x] Tasca 1.4: Crear test d'integració a `test/test\_tasks\_app.py` segons els escenaris GS-01, GS-02 i GS-03.

- [x] Tasca 1.5: Validar execució amb OpenCode i verificar que tots els tests passen (`python3 -m pytest test`).


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

- [x] Tasca 2.2: Ampliar add amb --due obligatori i validar dates.
  Mostrar el missatge especificat quan la data falta o és invàlida.
  Garantir IDs automàtics segons el màxim existent.
  Adaptar la prova de creació del primer increment.
  Afegir proves de dates vàlides, invàlides i absents.
  Requisits: RF-03, RF-05, RF-06 i RF-21.
  Escenaris: GS-01 adaptat, GS-04, GS-05 i GS-06.

### Modificació d’atributs

- [x] Tasca 2.3: Implementar setTitle i les proves corresponents.
  Verificar ID inexistent, persistència i conservació dels altres atributs.
  Requisits: RF-07, RF-11 i RF-20.
  Escenaris: GS-07 i GS-12 per a setTitle.

- [x] Tasca 2.4: Implementar setSubject i les proves corresponents.
  Verificar ID inexistent, persistència i conservació dels altres atributs.
  Requisits: RF-08, RF-11 i RF-20.
  Escenaris: GS-08 i GS-12 per a setSubject.

- [x] Tasca 2.5: Implementar setDueDate i les proves corresponents.
  Permetre assignar dates a tasques antigues.
  Verificar dates invàlides, ID inexistent i persistència.
  Requisits: RF-06, RF-09, RF-11 i RF-20.
  Escenaris: GS-09, GS-10 i GS-12 per a setDueDate.

- [ ] Tasca 2.6: Implementar setId i les proves corresponents.
  Verificar ID inexistent, duplicat, invàlid i igual a l’actual.
  Comprovar la creació de tasques després de canviar un ID.
  Requisits: RF-11, RF-16, RF-17, RF-18, RF-20 i RF-21.
  Escenaris: GS-12 per a setId, GS-16, GS-17, GS-18,
  GS-20 i la part de setId de GS-21.

### Canvis d’estat

- [ ] Tasca 2.7: Implementar completeTask i les proves corresponents.
  Verificar ID inexistent, persistència i repetició del comandament.
  Requisits: RF-10, RF-11 i RF-20.
  Escenaris: GS-11, GS-12 per a completeTask
  i la part de completeTask de GS-21.

- [ ] Tasca 2.8: Implementar markPending i les proves de canvi d’estat.
  Verificar ID inexistent, persistència i repetició del comandament.
  La comprovació dels avisos de GS-19 es farà a la tasca 2.9.
  Requisits: RF-11, RF-19 i RF-20.
  Escenaris: canvi d’estat de GS-19, GS-12 per a markPending
  i la part de markPending de GS-21.

### Llistat i validació

- [ ] Tasca 2.9: Ampliar list amb la data límit i els avisos.
  Mostrar "sense data" per a les tasques que no en tenen.
  Calcular els avisos segons la data local actual.
  Utilitzar una data controlada en les proves.
  Comprovar els límits d’avui, ahir, sis dies i set dies.
  Adaptar les proves del llistat del primer increment.
  Requisits: RF-04, RF-12, RF-13, RF-14 i RF-22.
  Escenaris: GS-02, GS-03 adaptat, GS-13, GS-14, GS-15
  i comprovació completa de GS-19.

- [ ] Tasca 2.10: Validar el segon increment complet.
  Executar python3 -m pytest test.
  Verificar la creació de data/tasks.json quan no existeix.
  Comprovar manualment tots els comandaments.
  Comprovar que els errors no modifiquen el registre.
  Confirmar la persistència entre execucions.
  Requisits: RF-01 a RF-22 amb les ampliacions de v2.0.
  Escenaris: GS-01 a GS-21 amb les adaptacions documentades.
