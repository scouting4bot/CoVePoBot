# CoVePoPhys
![License](https://img.shields.io/badge/status-not%20ready-red)

**n.b. la procedura è ancora vulnerabile e da revisionare**, non è pronta per un uso effettivo.

Panoramica
--------
**CoVePoPhys** è un insieme di procedure pensate per lo svolgimento delle funzioni di Verifica Poteri (CoVePo) in assemblee in presenza che richiedano voto digitalizzato con [ScrutinioFast](docs/istruzioni_scrutinio_ita.md). **Non è ottimizzato per le assemblee online**. CoVePoPhys permette di fornire ai votanti un codice autorizzativo da usare per il voto, garantendo a questi la segretezza e l'impossibilità di associare la loro identità con le preferenze espresse.
* Non necessita di installazione di nuovo software
* Si basa sulla piattaforma Google, ma può essere esportato su altri servizi analoghi (form+foglio di calcolo)
* Produce una lista di "secret" (una password segreta)
* Permette alla CoVePo di ottenere
  * la lista di "secret" attivati dagli utenti.

Acronimi, glossario e convenzioni
--------
* **CoVePo**: *Commissione Verifica Poteri*, è l'organo che si occupa dell'autenticazione ed autorizzazione degli utenti votanti.
* **Scrutinio**: è la procedura seguita per
	* la verifica della validità del voto (cioè che abbia votato solo chi ne aveva diritto)
	* il conteggio dei risultati di una votazione e la verifica della su
* **Secret**: è la password che autorizzerà l'utente a votare.
* **Votante**: è persona che partecipa all'assemblea con diritto di voto.

Predisposizione
--------
La CoVePo dovrà avere a disposizione un tablet, un ampio contenitore e dei foglietti.

 1. Creazione form di verifica poteri: creare un google form che prenda come input solo il secret della persona
 2. Aprire il foglio di calcolo associato ai risultati: qui saranno elencati i vari secret pian piano che si registrano.
 3. Preparare dei bigliettini arrotolati con scritto un codice (il secret) in ognuno.
 4. Versare in un contenitore ampio i bigliettini.

Procedure
--------
### Registrazione votante

 1. mi presento in covepo,
 2. mi registrano nella tabellina
 3. mi fanno pescare un biglietto da una scatola (tipo pesca di paese, con i foglietti arrotolati nella pasta)
 4. io votatore inserisco il numero in un tablet (un semplice google form per raccogliere i codici attivi il cui google fogli è accessibile a covepo con diritti di modifica)
**n.b.: da rivedere**, l'ordine della lista potrebbe associare il votante ed il secret.
 6. *[facoltativo]* una verifica che i codici inseriti nel form di covepo siano tra quelli messi nella scatola
 7. voto via google form (un form per ogni votazione)
 8. covepo consegna agli scrutatori la lista aggiornata di codici attivi
 9. scrutinio via google fogli con il sistema di controllo dell'altra volta

### Cancellazione votante
**n.b.: da rivedere, al momento non garantisce la segretezza**, per ora si consiglia di usare la procedura di verifica del numero legale.

 1. consegno in covepo il biglietto col codice
 2. alla votazione successiva la covepo fornisce agli scrutatori la nuova lista
### Verifica numero legale
Usabile anche nel caso un votante sia andato via senza comunicarlo alla CoVePo od abbia perso il proprio secret.

 1. cancelli i risultati del form di verifica poteri e chiedi un nuovo inserimento da parte dei presenti e consideri quella la nuova lista di codici
**n.b.: da rivedere**, l'url, diventato pubblico, potrebbe essere usato da persone non registrate per autenticare fraudolentemente secret non previsti.
