# SPECIFICATIONS.md — Sistema Tasks_app

## 1. Visió general

Tasks_app és una eina CLI per ajudar els estudiants a gestionar les seves
tasques acadèmiques.

Les dades es conserven entre execucions en el fitxer data/tasks.json.

## 2. Evolució del sistema

- Increment 1 — v1.0: creació i llistat de tasques.
- Increment 2 — v2.0: dates límit, modificació d’atributs, canvis d’estat
  i avisos d’urgència i caducitat.

# Increment 1 — v1.0

## 3. Històries d’usuari

- US-01: Com a estudiant, vull afegir una tasca amb títol i assignatura
  per recordar els meus deures.
- US-02: Com a estudiant, vull veure les tasques registrades
  per organitzar el meu temps.

## 4. Model de dades inicial

Cada tasca conté:

- id: enter positiu i únic.
- títol: text.
- assignatura: text.
- estat: pendent o completada.

## 5. Requisits inicials

- RF-01: El sistema tasks_app ha de guardar les tasques en un fitxer
  JSON de persistència local.
- RF-02: Si el fitxer data/tasks.json no existeix, el sistema tasks_app
  ha de crear-lo inicialitzat amb una llista JSON buida ([]).
- RF-03: El sistema tasks_app ha de proveir a l’estudiant la capacitat
  de crear una nova tasca amb estat pendent mitjançant
  add --title <títol> --subject <assignatura>.
- RF-04: El sistema tasks_app ha de proveir a l’estudiant la capacitat
  de visualitzar totes les tasques registrades, incloent-hi ID, títol,
  assignatura i estat, mitjançant list.

## 6. Escenaris inicials

### GS-01: Creació correcta d’una tasca
Atès que el registre de tasques és buit
Quan l’estudiant executa:
  python3 src/tasks_app.py add --title "Pràctica 1" --subject "RS"
Aleshores el sistema mostra "Tasca [ID: 1] creada amb èxit"
I la tasca queda registrada a data/tasks.json amb estat pendent.

### GS-02: Llistat buit
Atès que el registre de tasques és buit
Quan l’estudiant executa:
  python3 src/tasks_app.py list
Aleshores el sistema mostra "Registre de tasques buit.".

### GS-03: Llistat amb tasques
Atès que el registre conté:
  | id | títol          | assignatura | estat   |
  | 1  | Pràctica 1     | RS          | pendent |
  | 2  | Examen parcial | SO          | pendent |
Quan l’estudiant executa:
  python3 src/tasks_app.py list
Aleshores el sistema mostra:
  [1] Pràctica 1 (RS) - estat: pendent
  [2] Examen parcial (SO) - estat: pendent

# Increment 2 — v2.0

## 7. Històries d’usuari

- US-03: Com a estudiant, vull indicar la data límit d’una nova tasca
  per conèixer el termini de lliurament.
- US-04: Com a estudiant, vull modificar el títol, l’assignatura o la
  data límit d’una tasca per corregir o actualitzar la informació.
- US-05: Com a estudiant, vull marcar una tasca com a completada
  per registrar que ja l’he acabada.
- US-06: Com a estudiant, vull identificar les tasques urgents i caducades
  per prioritzar la feina.
- US-07: Com a estudiant, vull modificar l’ID d’una tasca
  per reorganitzar els seus identificadors.
- US-08: Com a estudiant, vull retornar una tasca completada a pendent
  per registrar que encara requereix feina.

## 8. Ampliació del model de dades

S’afegeix l’atribut:

- data_limit: data vàlida en format YYYY-MM-DD.

Les tasques noves han de tenir data límit.

Les tasques antigues poden tenir l’atribut absent o amb valor null.
En tots dos casos es consideren tasques sense data límit.

Els estats admesos són pendent i completada.

## 9. Comandaments

- Crear:
  add --title <títol> --subject <assignatura> --due <YYYY-MM-DD>
- Llistar:
  list
- Canviar el títol:
  setTitle --id <ID> --title <títol>
- Canviar l’assignatura:
  setSubject --id <ID> --subject <assignatura>
- Assignar o canviar la data límit:
  setDueDate --id <ID> --due <YYYY-MM-DD>
- Canviar l’identificador:
  setId --id <ID_actual> --newId <ID_nou>
- Completar:
  completeTask --id <ID>
- Retornar a pendent:
  markPending --id <ID>

En totes les operacions, --id identifica la tasca existent.

## 10. Regles de dates i avisos

La data de referència és la data local del sistema, sense considerar hores.

- Una tasca pendent amb data anterior a avui és CADUCADA.
- Una tasca pendent que venç avui o en els sis dies següents és URGENT.
- Una tasca que venç d’aquí a set dies encara no és URGENT.
- Una tasca completada no mostra avisos.
- Una tasca sense data límit no mostra avisos.
- Els avisos es calculen en llistar; no es desen com a estats.
- Una tasca no pot mostrar els dos avisos simultàniament.
- S’admeten dates passades, sempre que siguin dates vàlides.

## 11. Requisits del segon increment

RF-05 amplia RF-03: en la versió 2.0, --due és obligatori en crear
una tasca. L’historial de la versió 1.0 es conserva com a documentació.

- RF-05: El sistema tasks_app ha de requerir una data límit vàlida
  en format YYYY-MM-DD per crear una nova tasca mitjançant add.

- RF-06: Si una data introduïda no és vàlida o falta en crear una
  tasca, el sistema tasks_app ha de mostrar "error: fecha invalida"
  sense modificar les dades.

- RF-07: El sistema tasks_app ha de proveir a l’estudiant la capacitat
  de modificar el títol d’una tasca mitjançant
  setTitle --id <ID> --title <títol>.

- RF-08: El sistema tasks_app ha de proveir a l’estudiant la capacitat
  de modificar l’assignatura d’una tasca mitjançant
  setSubject --id <ID> --subject <assignatura>.

- RF-09: El sistema tasks_app ha de proveir a l’estudiant la capacitat
  d’assignar o modificar la data límit d’una tasca mitjançant
  setDueDate --id <ID> --due <YYYY-MM-DD>.

- RF-10: El sistema tasks_app ha de proveir a l’estudiant la capacitat
  de marcar una tasca com a completada mitjançant completeTask --id <ID>.

- RF-11: Si l’ID indicat no correspon a cap tasca, el sistema tasks_app
  ha de mostrar "error: id no encontrado" sense modificar les dades.

- RF-12: Si una tasca pendent té una data límit anterior a avui,
  el sistema tasks_app ha de mostrar [CADUCADA] en llistar-la.

- RF-13: Si una tasca pendent venç avui o en els sis dies següents,
  el sistema tasks_app ha de mostrar [URGENT] en llistar-la.

- RF-14: Si una tasca està completada, no té data límit o venç d’aquí
  a set dies o més, el sistema tasks_app ha de llistar-la sense avisos.

- RF-15: El sistema tasks_app ha de conservar les tasques antigues
  sense data límit sense assignar-los una data automàticament.

- RF-16: El sistema tasks_app ha de proveir a l’estudiant la capacitat
  de modificar l’identificador d’una tasca mitjançant
  setId --id <ID_actual> --newId <ID_nou>.

- RF-17: Si el nou ID pertany a una altra tasca, el sistema tasks_app
  ha de mostrar "error: id ya existente" sense modificar les dades.

- RF-18: Si el nou ID no és un enter positiu, el sistema tasks_app
  ha de mostrar "error: id invalido" sense modificar les dades.

- RF-19: El sistema tasks_app ha de proveir a l’estudiant la capacitat
  de retornar una tasca a l’estat pendent mitjançant markPending --id <ID>.

- RF-20: El sistema tasks_app ha de conservar en el fitxer JSON
  els canvis d’atributs i d’estat entre execucions.

- RF-21: El sistema tasks_app ha d’assignar a cada nova tasca un ID
  igual al màxim ID existent més un, o 1 si el registre és buit.

- RF-22: El sistema tasks_app ha de mostrar en el llistat la data límit
  de cada tasca, o el text "sense data" quan no en tingui.

## 12. Precisió de les operacions

- Modificar un atribut conserva tots els altres atributs.
- setId amb el mateix ID actual és una operació vàlida sense canvis.
- completeTask sobre una tasca completada conserva el seu estat.
- markPending sobre una tasca pendent conserva el seu estat.
- Retornar a pendent fa que els avisos es tornin a calcular al llistat.
- Les operacions per ID comproven primer que la tasca existeix.
- Els errors no afegeixen, eliminen ni modifiquen cap tasca.

Format del llistat en v2.0:

[ID] títol (assignatura) - estat: estat - data límit: YYYY-MM-DD [AVÍS]

Si no hi ha data, s’utilitza "sense data".
Si no hi ha avís, s’omet el sufix de l’avís.

## 13. Escenaris del segon increment

### GS-04: Crear una tasca amb data límit
Atès que el registre és buit
Quan l’estudiant executa:
  python3 src/tasks_app.py add --title "Pràctica 2" --subject "RS" --due 2026-12-01
Aleshores es crea la tasca amb ID 1, estat pendent i data_limit "2026-12-01"
I les dades es conserven després de tornar a executar l’aplicació.

### GS-05: Rebutjar dates invàlides
Atès que es coneix el contingut actual del registre
Quan l’estudiant intenta crear una tasca amb --due <valor>
Aleshores el sistema mostra "error: fecha invalida"
I el registre no es modifica.

Exemples de valor:
  | valor      |
  | 2026-02-30 |
  | 01/12/2026 |
  | text       |

### GS-06: Rebutjar una alta sense data
Atès que es coneix el contingut actual del registre
Quan l’estudiant executa add amb títol i assignatura però sense --due
Aleshores el sistema mostra "error: fecha invalida"
I no crea cap tasca.

### GS-07: Modificar el títol
Atès que existeix una tasca amb ID 1
Quan l’estudiant executa:
  python3 src/tasks_app.py setTitle --id 1 --title "Títol revisat"
Aleshores el seu títol passa a ser "Títol revisat"
I conserva els altres atributs
I el canvi persisteix entre execucions.

### GS-08: Modificar l’assignatura
Atès que existeix una tasca amb ID 1
Quan l’estudiant executa:
  python3 src/tasks_app.py setSubject --id 1 --subject "SO"
Aleshores la seva assignatura passa a ser "SO"
I conserva els altres atributs
I el canvi persisteix entre execucions.

### GS-09: Assignar o modificar una data
Atès que existeix una tasca amb ID 1
Quan l’estudiant executa:
  python3 src/tasks_app.py setDueDate --id 1 --due 2026-12-03
Aleshores la seva data_limit passa a ser "2026-12-03"
I conserva els altres atributs
I el canvi persisteix entre execucions.

Aquest escenari s’ha de verificar tant amb una tasca sense data
com amb una tasca que ja en tingui.

### GS-10: Rebutjar una modificació amb data invàlida
Atès que existeix una tasca amb ID 1
Quan l’estudiant executa:
  python3 src/tasks_app.py setDueDate --id 1 --due 2026-02-30
Aleshores el sistema mostra "error: fecha invalida"
I el registre no es modifica.

### GS-11: Completar una tasca
Atès que existeix una tasca pendent amb ID 1
Quan l’estudiant executa:
  python3 src/tasks_app.py completeTask --id 1
Aleshores el seu estat passa a ser completada
I conserva els altres atributs
I el canvi persisteix entre execucions.

### GS-12: Operacions sobre un ID inexistent
Atès que no existeix cap tasca amb ID 999
Quan l’estudiant executa una operació sobre --id 999
Aleshores el sistema mostra "error: id no encontrado"
I el registre no es modifica.

Aquest escenari s’ha de verificar amb setTitle, setSubject,
setDueDate, setId, completeTask i markPending,
utilitzant arguments nous vàlids.

### GS-13: Avisos segons la data límit
Atès que la data actual és 2026-11-23
I existeix una tasca pendent amb la data límit indicada
Quan l’estudiant executa list
Aleshores el llistat mostra l’avís esperat.

Exemples:
  | data límit | avís esperat |
  | 2026-11-22 | [CADUCADA]   |
  | 2026-11-23 | [URGENT]     |
  | 2026-11-29 | [URGENT]     |
  | 2026-11-30 | cap          |

### GS-14: Conservar les tasques antigues sense data
Atès que el registre conté tasques antigues amb data_limit absent o null
Quan l’estudiant executa list
Aleshores les tasques apareixen amb el text "sense data"
I no mostren [URGENT] ni [CADUCADA]
I no se’ls assigna cap data automàticament.

### GS-15: No mostrar avisos en tasques completades
Atès que la data actual és 2026-11-23
I el registre conté tasques completades amb dates límit
2026-11-22, 2026-11-23 i 2026-11-29
Quan l’estudiant executa list
Aleshores cap d’aquestes tasques mostra [URGENT] ni [CADUCADA].

### GS-16: Canviar l’ID
Atès que existeix una tasca amb ID 1
I no existeix cap tasca amb ID 5
Quan l’estudiant executa:
  python3 src/tasks_app.py setId --id 1 --newId 5
Aleshores la tasca passa a tenir ID 5
I deixa d’existir una tasca amb ID 1
I conserva els altres atributs
I el canvi persisteix entre execucions.

### GS-17: Rebutjar un ID duplicat
Atès que existeixen tasques amb ID 1 i ID 5
Quan l’estudiant executa:
  python3 src/tasks_app.py setId --id 1 --newId 5
Aleshores el sistema mostra "error: id ya existente"
I el registre no es modifica.

### GS-18: Rebutjar un ID nou invàlid
Atès que existeix una tasca amb ID 1
Quan l’estudiant executa setId --id 1 --newId <valor>
Aleshores el sistema mostra "error: id invalido"
I el registre no es modifica.

Exemples de valor:
  | valor |
  | 0     |
  | -2    |
  | abc   |
  | 1.5   |

### GS-19: Retornar una tasca completada a pendent
Atès que la data actual és 2026-11-23
I existeix una tasca completada amb ID 5 i data límit 2026-11-22
Quan l’estudiant executa:
  python3 src/tasks_app.py markPending --id 5
Aleshores el seu estat passa a ser pendent
I conserva els altres atributs
I el canvi persisteix entre execucions
I en llistar-la mostra [CADUCADA].

Repetir la comprovació amb data límit 2026-11-23,
esperant [URGENT], i sense data límit, esperant cap avís.

### GS-20: Crear després d’un canvi d’ID
Atès que el registre conté una única tasca amb ID 1
I l’estudiant canvia el seu ID a 5
Quan crea una nova tasca vàlida
Aleshores la nova tasca rep l’ID 6
I la tasca amb ID 5 es conserva.

### GS-21: Repetir operacions sense alterar altres dades
Atès que existeix una tasca amb ID 1
Quan l’estudiant executa setId --id 1 --newId 1
Aleshores el registre no canvia
I no es mostra cap error.

Quan executa completeTask dues vegades sobre aquesta tasca
Aleshores l’estat final és completada
I es conserven els altres atributs.

Quan executa markPending dues vegades sobre aquesta tasca
Aleshores l’estat final és pendent
I es conserven els altres atributs.

## 14. Adaptació de les proves del primer increment

- GS-01 s’adapta afegint --due amb una data vàlida.
- GS-02 continua vigent sense canvis.
- GS-03 conserva les comprovacions d’ID, títol, assignatura i estat,
  i adapta el format de sortida a v2.0.
- Les proves de RF-02 han de comprovar que l’aplicació crea
  data/tasks.json quan aquest fitxer no existeix.


# Increment 3 — v3.0

## Històries d’usuari

- US-09: Com a estudiant, vull consultar un resum del nombre de tasques
  per conèixer l’estat general de la meva feina.
- US-10: Com a estudiant, vull llistar les tasques d’una assignatura
  per centrar-me en la feina d’aquesta matèria.
- US-11: Com a estudiant, vull cercar tasques mitjançant una paraula
  del títol per trobar-les fàcilment.

## Comandaments

- Resum:
  list --summary
- Filtre per assignatura:
  list --subject <assignatura>
- Filtre per text del títol:
  list --keyword <text>
- Filtres combinats:
  list --subject <assignatura> --keyword <text>
- Resum filtrat:
  list --summary --subject <assignatura> --keyword <text>

## Regles del llistat

- list sense opcions conserva el comportament de la versió 2.0.
- El filtre d’assignatura compara el nom complet, ignorant majúscules
  i minúscules.
- El filtre del títol cerca el text indicat com a subcadena,
  ignorant majúscules i minúscules.
- Si es combinen filtres, una tasca ha de complir-los tots.
- Els filtres no modifiquen les dades.
- El resum s’aplica al conjunt seleccionat pels filtres.
- --summary mostra únicament els recomptes.
- Sense coincidències, el llistat mostra
  "No s'han trobat tasques amb aquests filtres."
- Un resum sense coincidències mostra tots els recomptes a zero.

Les tasques urgents i caducades són subconjunts de les pendents.
Per tant:
- total = pendents + completades.
- Les urgents i caducades no se sumen una altra vegada al total.
- Les tasques pendents sense data compten com a pendents,
  però no com a urgents ni caducades.

## Requisits

- RF-23: El sistema tasks_app ha de proveir a l’estudiant la capacitat
  de consultar el nombre total de tasques i el nombre de tasques
  pendents, completades, caducades i urgents mitjançant list --summary.

- RF-24: El sistema tasks_app ha de calcular els recomptes de tasques
  urgents i caducades aplicant les regles de dates de la versió 2.0.

- RF-25: El sistema tasks_app ha de proveir a l’estudiant la capacitat
  de filtrar les tasques per coincidència completa de l’assignatura,
  ignorant majúscules i minúscules, mitjançant list --subject <assignatura>.

- RF-26: El sistema tasks_app ha de proveir a l’estudiant la capacitat
  de filtrar les tasques que contenen el text indicat en el títol,
  ignorant majúscules i minúscules, mitjançant list --keyword <text>.

- RF-27: Si s’indiquen els dos filtres, el sistema tasks_app ha de
  seleccionar únicament les tasques que compleixen tots dos criteris.

- RF-28: Si s’utilitza --summary amb filtres, el sistema tasks_app
  ha de calcular els recomptes únicament sobre les tasques seleccionades.

- RF-29: Si un llistat filtrat no té coincidències, el sistema tasks_app
  ha de mostrar "No s'han trobat tasques amb aquests filtres.".

- RF-30: Si el conjunt seleccionat per al resum és buit, el sistema
  tasks_app ha de mostrar tots els recomptes a zero.

- RF-31: El sistema tasks_app ha de conservar les dades del registre
  sense modificacions en executar qualsevol consulta de llistat o resum.

## Escenaris Gherkin

### Dades comunes dels escenaris GS-22 a GS-28

Atès que la data actual és 2026-11-23
I el registre conté:
  | id | títol              | assignatura | estat      | data_limit |
  | 1  | Pràctica requisits | RS          | pendent    | 2026-11-22 |
  | 2  | Examen parcial     | RS          | pendent    | 2026-11-23 |
  | 3  | Pràctica processos | SO          | completada | 2026-11-20 |
  | 4  | Lectura tema 4     | SO          | pendent    | 2026-12-10 |
  | 5  | Revisió apunts     | RS          | pendent    | null       |

Cada escenari parteix d’aquestes dades sense modificacions.

### GS-22: Resum general
Quan l’estudiant executa:
  python3 src/tasks_app.py list --summary
Aleshores el sistema mostra:
  Total: 5
  Pendents: 4
  Completades: 1
  Caducades: 1
  Urgents: 1
I no mostra les files individuals de les tasques.

### GS-23: Filtrar per assignatura
Quan l’estudiant executa:
  python3 src/tasks_app.py list --subject "rs"
Aleshores el sistema mostra únicament les tasques amb ID 1, 2 i 5
I conserva el format i els avisos del llistat de la versió 2.0.

### GS-24: Filtrar per text del títol
Quan l’estudiant executa:
  python3 src/tasks_app.py list --keyword "PRÀCTICA"
Aleshores el sistema mostra únicament les tasques amb ID 1 i 3.

### GS-25: Combinar filtres
Quan l’estudiant executa:
  python3 src/tasks_app.py list --subject "RS" --keyword "pràctica"
Aleshores el sistema mostra únicament la tasca amb ID 1.

### GS-26: Resum filtrat
Quan l’estudiant executa:
  python3 src/tasks_app.py list --summary --subject "RS"
Aleshores el sistema mostra:
  Total: 3
  Pendents: 3
  Completades: 0
  Caducades: 1
  Urgents: 1

### GS-27: Filtre sense coincidències
Quan l’estudiant executa:
  python3 src/tasks_app.py list --subject "BD"
Aleshores el sistema mostra
  "No s'han trobat tasques amb aquests filtres.".

### GS-28: Resum sense coincidències
Quan l’estudiant executa:
  python3 src/tasks_app.py list --summary --subject "BD"
Aleshores el sistema mostra:
  Total: 0
  Pendents: 0
  Completades: 0
  Caducades: 0
  Urgents: 0

### GS-29: Consultes sense modificar les dades
Atès que es coneix el contingut de data/tasks.json
Quan l’estudiant executa els llistats i resums del tercer increment
Aleshores el contingut de data/tasks.json no es modifica.

### GS-30: Resum d’un registre buit
Atès que el registre no conté tasques
Quan l’estudiant executa:
  python3 src/tasks_app.py list --summary
Aleshores el sistema mostra tots els recomptes a zero.