# ScrutinioFast
![License](https://img.shields.io/badge/status-work%20in%20progress-yellowgreen)

Panoramica
--------
**ScrutinioFast** è un insieme di procedure pensate per velocizzare lo scrutinio di voti assembleari, permettendo anche l'autenticazione del voto attraverso dei codici autorizzativi (secret).
I codici autorizzativi (o secret) devono essere consegnati ai votanti garantendo la segretezza, cioè che in qualsiasi fase non sia possibile dal singolo secret risalire all'identità del votante. Per la consegna dei secret possono essere usati [CoVePoPhys](istruzioni_CoVePoPhys_ita.md) (per le assemblee in presenza) o [CoVePoBot](istruzioni_CoVePoBot_ita.md) (per le assemblee online).

Acronimi, glossario e convenzioni
--------
* **CoVePo**: *Commissione Verifica Poteri*, è l'organo che si occupa dell'autenticazione ed autorizzazione degli utenti votanti.
* **Scrutinio**: è la procedura seguita per
	* la verifica della validità del voto (cioè che abbia votato solo chi ne aveva diritto)
	* il conteggio dei risultati di una votazione e la verifica della su
* **Votante**: è persona che partecipa all'assemblea con diritto di voto.

Predisposizione
--------
### Modulo di voto
Quanto segue va ripetuto per ogni modulo di voto (form) che sarà necessario nell'assemblea.
 - **Crea un nuovo form**
 - Inserisci un titolo
 - Inserisci una descrizione
 - **Prima domanda**
	 - come domanda inserisci un testo in cui inviti l'utente ad inserire il suo codice autorizzativo (seret).
	 - nel menù a tendina a destra seleziona l'opzione "*Risposta breve*".
	 - in basso a destra del box della domanda attiva il campo "*Obbligatorio*". 
	 - in basso a destra del box della domanda c'è un menù "a kebab" (tre puntini verticali): selezionalo e spunta l'opzione "*Convalida della risposta*".
	 - nelle nuove opzioni che si sono attivate inserisci le regole per la validazione del secret.
	 esempi:
		 - **Secret di 6 cifre numerico**: seleziona "*Espressione regolare*" e "*Corrispondenze*" ed aggiungi come patterna il seguente testo
			```text
			^[0-9]{6}$
			```
		 - **Secret di 10 cifre alfanumerico** (maiuscole e minuscole): seleziona "*Espressione regolare*" e "*Corrispondenze*" ed aggiungi come patterna il seguente testo
			```text
			^[a-zA-Z0-9]{10}$
			```
 - **Seconda domanda**
	 - clicca sul simbolo del "*+*" cerchiato nel menù a destra: ti aggiungerà una nuova domanda.
	 - scegli liberamente il contenuto del campo "*Domanda*". Questo, insieme alla descrizione, andrà a comporre il tuo quesito.
	 - in basso a destra del box della domanda attiva il campo "*Obbligatorio*". 
	 - tipologie di votazione: ricorda sempre di prevedere l'opzione di scelta "*Scheda bianca*".
		 - **una sola preferenza**: seleziona dal menù a tendina a destra la tipologia "*Scelta multipla*". Questo permetterà una sola selezione/preferenza.
		 - **multiple preferenze**: seleziona dal menù a tendina a destra la tipologia "*Caselle di controllo*". Questo permetterà più preferenze. 
			 - Se si vuole, si può aggiungere una "*Convalida della risposta*" che permette di definire il numero minimo e massimo di opzioni selezionabili.
 - **Foglio di calcolo**
	 - Seleziona il tab "*Risposte*" dal menù in alto.
	 - Seleziona l'icona di *Google Fogli* (è un quadrato verde con una croce bianca): ti creerà un foglio di lavoro con le risposte del form. Per pulizia di lavoro, conviene creare un foglio di lavoro per ogni form.
	 - Aprire il foglio di calcolo associato ai risultati del form: ci dovrebbe essere un foglio di calcolo nominato "*Risposte del modulo 1*".
	 - Aggiungere due fogli:
		 -  *Autenticazione e Scrutinio*: qui verranno fatte le operazioni di validazione ed autenticazione dei voti e lo scrutinio vero e proprio.
		 - *Elenco secret*: qui verranno elencati i secret autorizzati dalla Verifica Poteri.

### Verifica voti duplicati
Evidenzierà i secret utilizzati per più di una votazione. Sarà a carico dello scrutatore decidere se eliminare tutte le votazioni o se ammettere l'ultima in ordine cronologico.
 - Aprire il foglio **Autenticazione e Scrutinio**
	 - nella casella E2 incollare il seguente testo:
		```text
		Controllo 1: voti duplicati
		```
	 - nella casella E3 incollare il seguente testo: creerà un filtro di tutti i secret duplicati (cioè che sono stati usati per votare più di una volta).

		```text
		=FILTER('Risposte del modulo 1'!B:B;COUNTIF('Risposte del modulo 1'!B:B;'Risposte del modulo 1'!B:B)>1)
		```

### Verifica voti non autorizzati
Evidenzierà i secret non autorizzati dalla Verifica Poteri. Sarà a carico dello scrutatore decidere se eliminare tali voti o sottrarli dai risultati dello scrutinio.
 - Aprire il foglio *Elenco secret*
	 - incollare nella colonna "A" (a partire dalla casella A1) tutti i secret forniti dalla Verifica Poteri. **Tale elenco va aggiornato prima di ogni votazione**.
 - Aprire il foglio *Autenticazione e Scrutinio*
	 - nella casella F2 incollare il seguente testo:
		```text
		Controllo 2: voto non autorizzato
		```
	 - nella casella F3 incollare il seguente testo: creerà un filtro di tutti i secret non autorizzati dalla Verifica Poteri.
		```text
		=FILTER('Risposte del modulo 1'!B:B;IFERROR(VLOOKUP('Risposte del modulo 1'!B:B;'Elenco secret'!A:A;1;0);TRUE))
		```

### Scrutinio dei voti
Evidenzierà i candidati votati con il conteggio delle relative preferenze.
 - Aprire il foglio *Autenticazione e Scrutinio*
	 - nella casella G2 incollare il seguente testo:
		```text
		Elenco Candidati
		```
	 - nella colonna G, a partire dalla casella G3, riportare i nomi dei candidati (o delle opzioni di voto).
	 - nella casella H2 incollare il seguente testo:
		```text
		Preferenze
		```
	 - nella colonna H, a partire dalla casella H3, incollare il seguente testo a destra di ogni casella piena nella colonna G: creerà un conteggio di tutti i voti espressi.
		```text
		=COUNTIF('Risposte del modulo 1'!C:C;"*"&G3&"*")
		```

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
