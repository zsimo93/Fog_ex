# API HTTP

### /api/actions
Metodo | Descrizione | Parametri | Codice e descrizione risposta
---|---|---|---
GET | Restituisce la lista delle azioni già create \hspace{3cm |  | 200 ({"actions": [])   
*POST* | Crea una nuova azione | type, name, description, in/out, language, containerTag*, cloud, timeout, file | 200 (Creato), 400 (richiesta incorretta), 406 (Nome già in uso)  

### /api/actions/_name_
Metodo | Descrizione | Parametri | Codice e descrizione risposta
---|---|---|---
DELETE | Elimina l'azione name | token | 200 (Eliminato), 202 (Sono presenti dipendenze), 406 (Nessuna azione con nome token)  
 
Nel caso l'azione presenti dipendenze, viene ritornato, con codice 202, la lista delle sequenze che dipendono da questa e un token che può essere usato per confermare la scelta di eliminare l'azione (\{"dependencies": [], "token": ""\). Rimandando la stessa richiesta con il token inserito in un Payload JSON, verrà eliminata l'azione e anche tutte le dipendenze citate nell'elenco.

### /api/sequences
Metodo | Descrizione | Parametri | Codice e descrizione risposta
---|---|---|---
GET | Restituisce la lista delle sequenze già create |  | 200 ({"sequences": [])   
POST | Crea una nuova sequenza |type, name, description, in/out, sequence | 200 (Creato), 400 (richiesta incorretta), 406 (Nome già in uso)  


### /api/sequences/_name_
Metodo | Descrizione | Parametri | Codice e descrizione risposta
---|---|---|---
DELETE | Elimina la sequenza name | token | 200 (Eliminato), 202 (Sono presenti dipendenze), 406 (Nessuna azione con nome token) 

Questo metodo ha lo stesso comportamento descritto per l'eliminazione delle azioni.

### /api/invoke
Metodo | Descrizione | Parametri | Codice e descrizione risposta
---|---|---|---
POST| Invoca una azione o una sequenza | name, param, default, except*, optimise*, log* | 200 (Eseguito), 400 (richiesta incorretta), 406 (Nome o parametri non validi), 500 (Errore nell'esecuzione)  

La risposta a questa invocazione sarà in formato JSON, con i campi specificati al momento della creazione della azione o sequenza invocata, più, se richiesto, un campo "log" contenente l'intero log di esecuzione.

### /api/nodes
Metodo | Descrizione | Parametri | Codice e descrizione risposta
---|---|---|---
GET | Restituisce la lista dei nodi nel sistema e le loro risorse |  | 200 ({"nodes": [])  
POST | Aggiunge un nuovo nodo al sistema | type, name, architecture, role, ip  | 200 (Creato), 400 (richiesta incorretta), 406 (Nome già in uso)  


### /api/nodes/_name_
Metodo | Descrizione | Parametri | Codice e descrizione risposta
---|---|---|---
DELETE | Elimina il nodo con nome name |  | 200 (Eliminato), 406 (Nessun nodo con nome token)  


### /api/aws
Metodo | Descrizione | Parametri | Codice e descrizione risposta
---|---|---|---
POST | Aggiunge nuove credenziali AWS | accessKeyID, secretAccessID, ARN | 200 (Creato), 400 (Richiesta incorretta)  
GET | Verifica la presenza di credenziali AWS | | 200 (Se presenti restituisce accessKeyID) 
DELETE | Rimuove le credenziali AWS | | 200 (OK) 


### /api/file
Metodo | Descrizione | Parametri | Codice e descrizione risposta
---|---|---|---
*POST* | Carica un nuovo file | file | 200 (Il file è salvato e viene restituito l'id a cui è stato assegnato), 400 (richiesta incorretta) 


### /api/file/_token_
Metodo | Descrizione | Parametri | Codice e descrizione risposta
---|---|---|---
GET | Scarica il file con id token | | 200 (File)  
DELETE | Elimina il file con id token |  | 200 (OK) 
