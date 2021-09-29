
# CoVePoPhys
![License](https://img.shields.io/badge/status-not%20ready-red)

**n.b. la procedura è ancora vulnerabile e da revisionare**, non è pronta per un uso effettivo.

Panoramica
--------
**CoVePoPhys** è un insieme di procedure pensate per lo svolgimento delle funzioni di Verifica Poteri (CoVePo) in assemblee in presenza che richiedano voto digitalizzato con [ScrutinioFast](istruzioni_ScrutinioFast_ita.md). **Non è ottimizzato per le assemblee online**. CoVePoPhys permette di fornire ai votanti un codice autorizzativo da usare per il voto, garantendo a questi la segretezza e l'impossibilità di associare la loro identità con le preferenze espresse.
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
	* il conteggio dei risultati di una votazione
* **Secret**: è la password che autorizzerà l'utente a votare.
* **Votante**: è persona che partecipa all'assemblea con diritto di voto.

Procedure Passo Passo
--------
Le istruzioni su cosa devono fare i membri della CoVePo nello svolgimento del loro ruolo.

### Prima dell'assemblea
 1. [Predispongono](#predisposizione) i moduli (detti *form*) di verifica poteri, la lista dei codici personali da consegnare (detti *secret*) ed i contenitori per l'assegnazione dei secret.
 n.b.: il modulo deve avere l'opzione "*Accetta risposte*" bloccata.
### In assemblea
 2. [Registrano i votanti](#registrazione-votante) e consegnano i secret di voto.
 3. Quando una singola votazione è dichiarata chiusa dalla presidenza di assemblea, comunicano agli scrutatori [la lista di *secret* autorizzati per quella votazione](#estrazione-secret-abilitati).
 4. Quando un votante lascia l'assemblea, devono procedere istantaneamente alla [cancellazione del votante](#cancellazione-votante).
 6. Qualora fosse necessario, possono coordinare la [verifica poteri e del numero legale](#verifica-numero-legale).

Predisposizione
--------
Oltre all'ordinario materiale, la CoVePo dovrà avere a disposizione:

 - un tablet con connessione ad internet
 - un ampio contenitore per ogni votazione da svolgere
 - dei foglietti colorati (un colore per ogni votazione da svolgere).

Ogni (form di) votazione richiederà un secret diverso. Per comodità conviene associare un colore ad ogni votazione, così da ridurre la confusione negli utenti.
 1. Concordare con gli scrutatori il formato dei codici personali (*secret*): lunghezza e composizione (alfanumerico, numerico, alfabetico maiuscolo, etc).
 2. Creazione di una lista di codici *secret* nel formato concordato. Va creata una lista diversa per ogni votazione.
 3. Concordare con gli scrutatori  il colore associato ad ogni singolo form di voto.
 4. Preparare dei bigliettini riportando un codice (il secret) in ognuno. Ogni bigliettino dovrebbe avere associato il colore della votazione in cui va usato (può essere lo sfondo del cartoncino od il colore usato per scriverlo).
 5. Creazione form di verifica poteri
	 - Seleziona il tab "*Risposte*" dal menù in alto.
	 - Disattiva l'opzione "*Accetta risposte*" a destra: questo eviterà l'inserimento di valori finché la registrazione in CoVePo non sarà aperta.
	- Inserisci un titolo
    - Inserisci una descrizione
    - Inserire un campo di input per ogni sessione di voto. Usa il colore per aiutare a capire quale codice vada in quale campo.
		 - nel menù a tendina a destra seleziona l'opzione "*Risposta breve*".
		 - in basso a destra del riquadro della domanda devi attivare il campo "*Obbligatorio*". 
		 - in basso a destra del riquadro della domanda c'è un menù "*a kebab*" (tre puntini verticali): selezionalo e spunta l'opzione "*Convalida della risposta*".
		 - nelle nuove opzioni che si sono attivate inserisci le regole per la validazione del secret.
		 esempi:
			 - **Secret di 6 cifre numerico**: seleziona "*Espressione regolare*" e "*Corrispondenze*" ed aggiungi come *pattern* il seguente testo
				```text
				^[0-9]{6}$
				```
			 - **Secret di 6 caratteri alfabetici maiuscoli**: seleziona "*Espressione regolare*" e "*Corrispondenze*" ed aggiungi come *pattern* il seguente testo
				```text
				^[A-Z]{6}$
				```
			 - **Secret di 10 cifre alfanumerico** (maiuscole e minuscole): seleziona "*Espressione regolare*" e "*Corrispondenze*" ed aggiungi come *pattern* il seguente testo
				```text
				^[a-zA-Z0-9]{10}$
				```
	    - ripeti per ogni colore.
 6. Versare i bigliettini nei contenitori. Ogni contenitore conterrà tutti i biglietti relativi ad solo colore.

Estrazione secret abilitati
--------
 - Dal form di verifica poteri, accedere al **Foglio di calcolo**
	 - Seleziona il tab "*Risposte*" dal menù in alto.
	 - Seleziona l'icona di *Google Fogli* (è un quadrato verde con una croce bianca): ti creerà un foglio di lavoro con le risposte del form. Per pulizia di lavoro, conviene creare un foglio di lavoro per ogni form.
	 - Aprire il foglio di calcolo associato ai risultati del form: ci dovrebbe essere un foglio di calcolo nominato "*Risposte del modulo 1*".
	 - Ogni colonna corrisponde alla lista di secret di un colore diverso (1° coloere > colonna A, 2° colore > colonna B, etc).

Gestione votanti
--------
### Registrazione votante
 1. **Attivare il form**
	 - Seleziona il tab "*Risposte*" dal menù in alto.
	 - Attiva l'opzione "*Accetta risposte*" a destra.
 2. **Registrazione**: quando arriva il votante, va aggiornato nel registro della CoVePo con eventuale delega.
 3. **Assegnazione secret**: il votante deve pescare da ogni contenitore un solo biglietto (due se ha una delega) per ogni colore.
 4. **Attivazione secret**: al votatore viene consegnato il tablet con aperto il form di verifica poteri. Il votatore inserisce tutti i suoi codici (se ha una delega deve ripetere l'inserimento una seconda volta).
**n.b.: da rivedere**, l'ordine della lista potrebbe associare il votante ed il secret, soprattutto in fase di cancellazione.
 6. *(facoltativo)* la CoVePo verifica che i codici inseriti nel form di covepo siano tra quelli messi nella scatola (con una formula simile a quella prevista per la [verifica dei voti non autorizzati](istruzioni_ScrutinioFast_ita.md#verifica-voti-non-autorizzati))

### Cancellazione votante
**n.b.: da rivedere, al momento non garantisce la segretezza**, per ora si consiglia di usare la procedura di verifica del numero legale.

 1. Il votante informa la CoVePo che sta lasciando l'assemblea e consegna i biglietit con i *secret* delle votazioni non ancora svolte.
 2. La CoVePo aggiorna il registro e sottrae dalla lista di codici autorizzati quelli relativi al votante che sta uscendo.

### Verifica numero legale
Usabile anche nel caso un votante sia andato via senza comunicarlo alla CoVePo od abbia perso il proprio secret.

 1. Salvare il vecchio risultato in un altro file (*backup*).
 2. Cancellare il vecchio risultato dal foglio di calcolo del form di verifica poteri e chiedi un nuovo inserimento da parte dei presenti.
 3. Quella ottenuta sarà da ora considerata la nuova lista di codici attivati.
**n.b.: da rivedere**, l'url, diventato pubblico, potrebbe essere usato da persone non registrate per autenticare fraudolentemente secret non previsti. Un consiglio è predisporre un forma a parte per gestire queste eventualità.
