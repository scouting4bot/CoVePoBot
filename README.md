
# CoVePoBot - Ensemble
![License](https://img.shields.io/badge/status-work%20in%20progress-red) ![License](https://img.shields.io/badge/version-0.2.2-yellow) ![License](https://img.shields.io/github/languages/top/scouting4bot/CoVePoBot)

Panoramica
--------
**CoVePoBot - Ensemble** è un supporto pensato per la digitalizzazione delle assemblee associative.
Esso si divide in diverse offerte:

 - **CoVePoBot**: applicazione web in python ([flask](https://flask.palletsprojects.com/)) per lo svolgimento delle funzioni di Verifica Poteri (CoVePo) in **assemblee online**. CoVePoBot permette di fornire ai votanti un codice autorizzativo da usare per il voto, garantendo a questi la segretezza e l'impossibilità di associare la loro identità con le preferenze espresse. Non è ottimizzato per le assemblee in presenza (in questi casi si suggerisce l'uso delle procedure tradizionali o, in caso di scrutinio automatizzato, quanto riportato per [CoVePoPhys](docs/istruzioni_CoVePoPhys_ita.md)).
	 - [Guida ed approfondimenti](docs/istruzioni_CoVePoBot_ita.md)
 - **CoVePoPhys**: procedure di Covepo per lo svolgimento delle funzioni di Verifica Poteri (CoVePo) in **assemblee in presenza**. Non è ottimizzato per le assemblee online (in questi casi si suggerisce l'uso di [CoVePoBot](docs/istruzioni_CoVePoBot_ita.md)).
	 - [Guida ed approfondimenti](docs/istruzioni_CoVePoPhys_ita.md)
 - **ScrutinioFast**: foglio di calcolo per lo scrutinio automatizzato del voto.
	 - [Guida ed approfondimenti](docs/istruzioni_scrutinio_ita.md)

Acronimi, glossario e convenzioni
--------
* **CoVePo**: *Commissione Verifica Poteri*, è l'organo che si occupa dell'autenticazione ed autorizzazione degli utenti votanti.
* **Scrutinio**: è la procedura seguita per
	* la verifica della validità ed autenticazione del voto (cioè che abbia votato solo chi ne aveva diritto)
	* il conteggio dei risultati di una votazione e la verifica della su
* **Votante**: è persona che partecipa all'assemblea con diritto di voto.

Come scegliere
--------
Non tutte le soluzioni sono applicabili ad ogni contesto. Molto dipende dalla modalità in cui sarà svolta la verifica poteri ed il voto+scrutinio. Di seguito una tabella che (dovrebbe) semplificare la scelta:
|  |CoVePo|Voto|Soluzione adatta||
|--|--|--|--|--|
|  | online  | online  | [CoVePoBot](docs/istruzioni_CoVePoBot_ita.md)+[ScrutinioFast](docs/istruzioni_scrutinio_ita.md) ||
|  | in presenza | online | [CoVePoPhys](docs/istruzioni_CoVePoPhys_ita.md)+[ScrutinioFast](docs/istruzioni_scrutinio_ita.md) ||
|  | ~~online~~  | ~~in presenza~~ | ~~[CoVePoBot](docs/istruzioni_CoVePoBot_ita.md)~~+**n.d.** |*|
|  | in presenza | in presenza | [CoVePoPhys](docs/istruzioni_CoVePoPhys_ita.md)+[ScrutinioFast](docs/istruzioni_scrutinio_ita.md) oppure le procedure tradizionali cartacee ||
|  | | |  ||
* n.d.: non è disponibile una soluzione integrata per il caso di scrutinio on presenza a valle di operazioni di verifica poteri online non è disponibile.
Sviluppi futuri
--------
* **Guide**: migliorare le guide
	* [ ] implementare una piccola wiki
	* [ ] aggiungere alla guida la parte della dashboard e liste csv
* **CoVePoBot**
	* migliorare la sicurezza
		* [ ] non gestire la password di amministrazione in chiaro sull'URL
		* [ ] migliorare l'algoritmo di conversione dell'OTP in Secret
		* [ ] test
	* performance
		* [x] non ripetizione OTP
		* [x] non ripetizione Secret
		* [ ] test
	* user-friendly:
		* [ ] pagina per conversione otp (inserisco OTP ed ottengo il secret senza dover comporre l'url ad-hoc)
		* [ ] pulsante di copia del secret
		* [ ] evitare 'l' minuscola, per evitare che si confonda con un '1'
		* [ ] evitare 'O' maiuscola, per evitare che si confonda con uno '0'
		* [ ] test
	* restful
		* [ ] avendo implementato la dashboard, si potrebbero rendere restful le API esposte
		* [ ] test
	* installazione
		* [ ] prevedere procedure guidate di installazione per qualche piattaforma di hosting gratuita
* **CoVePoBot**
	* migliorare la sicurezza
		* [ ] gestione della cancellazione di una utenza
* **ScrutinioFast**
	* [ ] template su foglio di calcolo per lo scrutinio

Versione
--------
*  v. 0.2.*
	* non ripetizione OTP e Secret
	* aggiornamento README
*  v. 0.1.*
	* versione di partenza
