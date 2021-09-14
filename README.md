

# CoVePoBot v. 0.1

Panoramica
--------
CoVePoBot è un supporto pensato per le funzioni di Verifica Poteri (CoVePo) in assemblee digitalizzate.
Con CoVePoBot è possibile fornire ai votanti un codice autorizzativo garantendo la segreteza del loro voto e l'impossibilità di risalire all'identità del votante.
* Funziona via browser (eg. chrome)
* Non necessita di sottoscrizione
* Produce una lista di password mono-uso (OTP: one time password)
* Converte gli OTP in "secret" (una password segreta)
* Converte una sola volta lo stesso OTP: se lo perdi sei fregato. Se qualcuno converte l'otp fraudolentemente, la CoVePo può disattivare il relativo secret con l'otp.
* Permette alla CoVePo di ottenere
  * la lista di OTP ancora non convertiti
  * la lista di "secret" attivati dall'utente.

Acronimi, glossario e convenzioni
--------
* **CoVePo**: *Commissione Verifica Poteri*, è l'organo che si occupa dell'autenticazione ed autorizzazione degli utenti votanti.
* **OTP**: *One Time Password*, *numerico*, è una sequenza numerica usa e getta (non è possibile usarla più volte). Viene fornita dalla CoVePo all'utente per convertirla nella password segreta (Secret) da usare in fase di votazione. Questo garantisce la segretezza del voto poiché la CoVePo non sarà in grado di associarlo al votante.
* **Secret**: è la password che autorizzerà l'utente a votare.
* **URL**: *Uniform Resource Locator* è una sequenza di caratteri che identifica univocamente l'indirizzo di una risorsa (documento, immagine, servizio, API) su una rete ([Wikipedia](https://it.wikipedia.org/wiki/Uniform_Resource_Locator))
* **DOMINIO**: negli esempi che seguono, gli url riportati possono essere testati sostituendo "*DOMINIO*" con "*effedici.pythonanywhere.com*"
* Negli esempi che seguono è stata usata la seguente convenzione:
  * **XXX** = *alfanumerico*, è il nome della sessione (influirà sugli url per la conversione)
  * **YYY** = *numerico*, è il numero di otp da attivare
  * **ZZZ** = *alfanumerico*, è la password di amministrazione fornita da CoVePoBot alla creazione della nuova sessione di voto
  * **OOO** = *numerico*, è l'OTP da convertire in secret
  * **SSS** = *alfanumerico*, è il secret ottenuto dalla conversione dell'OTP

Amministrazione
--------
### Creazione di una nuova sessione di voto ###
(es: un'assemblea)
* La CoVePo può attivare una nuova sessione di voto invocando l'url
```url
 http://DOMINIO/CoVePoBot/session?id=XXX&otp_num=YYY
```
* esempio di risposta:
  > Aggiunta la nuova sessione XXX. Usa come password per la gestione: ZZZ
  > Gli otp disponibili sono: 123456,234567,345678,456789,567890
* Aggiungendo il parametro 'otp_as_url' è possibile ottenere la lista degli otp in forma di url già composto
```url
http://DOMINIO/CoVePoBot/session?id=XXX&otp_num=YYY&otp_as_url=true
```
* esempio di risposta:
  > Aggiunta la nuova sessione XXX. Usa come password per la gestione: ZZZ
  > Gli otp disponibili sono:
  > https://DOMINIO/CoVePoBot/XXX/otp/123456
  > https://DOMINIO/CoVePoBot/XXX/otp/234567

### Recupero della lista di "secret" attivati ###
* La CoVePo può recuperare la lista dei secret attivati dagli utenti.
```url
http://DOMINIO/CoVePoBot/XXX/secrets?password=ZZZ
```
* esempio di risposta:
  >as5d64fr97,b69b91a53a
* Un secret si attiva convertendo l'OTP all'opportuno URL
* Da un secret non è possibile risalite all'OTP convertito

### Recupero della lista di OTP non convertiti ancora dagli utenti ###
* La CoVePo può recuperare la lista degli OTP non ancora attivati dagli utenti.
```url
http://DOMINIO/CoVePoBot/XXX/otps/?password=ZZZ
```
* esempio di risposta:
  > 234567,345678,456789,567890

### Aggiunta di ulteriori OTP alla sessione di voto ###
* La CoVePo può aggiungere nuovi OTP alla sessione di voto.
```url
http://DOMINIO/CoVePoBot/XXX/additionalotp/?password=ZZZ&otp_num=YYY
```
* esempio di risposta:
  > La sessione XXX è stata aggiornata.
  > I nuovi otp disponibili sono: 098765,987654,876543
* Aggiungendo il parametro '*otp_as_url*' è possibile ottenere la lista degli otp in forma di url già composto
```url
http://DOMINIO/CoVePoBot/XXX/additionalotp/?password=ZZZ&otp_num=YYY&otp_as_url=true
```
* esempio di risposta:
  > La sessione XXX è stata aggiornata.
  > I nuovi otp disponibili sono:
  > https://DOMINIO/CoVePoBot/XXX/otp/123456
  > https://DOMINIO/CoVePoBot/XXX/otp/234567

### Rimozione di un secret ###
* La CoVePo può annullare un secret a partire dal relativo OTP.
```url
http://DOMINIO/CoVePoBot/XXX/secret/OOO/?password=ZZZ
```
* esempio di risposta:
  > Secret disabilitato

Come si attiva l’OTP
--------
* L'utente dovrà chiamare un URL da browser come il seguente (sostituire OOO con l'OTP)
```url
http://DOMINIO/CoVePoBot/XXX/otp/OOO
```
* esempio di risposta:
  > Il tuo codice è SSS e ti servirà per votare alla XXX.
  > Attenzione! Non sarà possibile riprodurlo nuovamente. Perciò conservalo accuratamente e non perderlo

* Si suggerisce che la CoVePo fornisca direttamente il link completo poiché non tutti gli utenti sono in grado di costruire un URL.

Installazione
--------
### N.B.: non è stato ancora possibile testare integralmente il codice in un ambiente ad-hoc. Per questo motivo si potrebbe riscontrare piccoli problemi di connettività con il DB mySQL. ###
### N.B.: Per l'installazione su Heroku, è previsto un branch ad-hoc (master_heroku) da utilizzare. ###
* Codice: al momento non è disponibile un pacchetto di rilasico. Copiare il codice di questo repository.
* Configurazioni: è possibile configurare l'applicativo con gli opportuni JSON indicati di seguito. Qualora si volessero usare variabili d'ambiente per sovrascrivere le configurazioni, si raccomanda di aggiungere la variabile d'ambiente "has_config_vars" con valore "true" per attivarne l'uso.
	* Database: nel caso in cui si usi un DB mySQL, connettersi al Database ed eseguire i comandi presenti nella cartella '/CoVePoBot/static/sql'.

	* Installare le dipendenze presenti nel file "/requirements.txt" con pip oppure creando un "environment" python.
		> es.:
		> mkvirtualenv myvirtualenv --python=/usr/bin/python3.7
		> workon myvirtualenv
		> pip install flask
		> pip install requests
		> pip install flask-mysql

	* Modificare le informazioni presenti nel JSON di configurazione 'CoVePoBot/static/conf/app.json'. In particolare è necessario compilare i seguenti campi:
		* "domain": con il dominio su cui sarà raggiungibile l'applicativo. Ad esempio se si scrive "domain": "www.mysite.com", vorrà dire che l'applicativo risponderà a www.mysite.com/CoVePoBot/session
		* "use_db": con un valore "True" o "False" a seconda che si usi rispettivamente un Database o non se ne faccia uso.

		* Tutti i campi che iniziano con "MYSQL_DATABASE_" saranno necessari solo se si userà un Database (mySQL)
			* "MYSQL_DATABASE_HOST" è l'host del DB.
			* "MYSQL_DATABASE_PORT": è la porta a cui connettersi per l'accesso al DB.
			* "MYSQL_DATABASE_USER": è l'utente per l'accesso al DB.
			* "MYSQL_DATABASE_PASSWORD": è la password per l'accesso dell'utente al DB.


Piattaforma
--------
* L'applicativo è scritto in Python con Framework Flask.
* Al momento non sono previste versioni specifiche per ogni piattaforma.
* Una istanza d'esempio (non manutenuta) è disponibile al dominio
  > effedici.pythonanywhere.com

Sviluppi futuri
--------
* migliorare la guida
	* [ ] implementare una piccola wiki
	* [ ] aggiungere alla guida la parte della dashboard e liste csv
* migliorare la sicurezza
	* [ ] non gestire la password in chiaro
* performance
	* [x] non ripetizione OTP
	* [ ] non ripetizione Secret
* user-friendly:
	* [ ] evitare 'l' minuscola, per evitare che si confonda con un '1'
	* [ ] evitare 'O' maiuscola, per evitare che si confonda con uno '0'
* restful
	* [ ] avendo implementato la dashboard, si potrebbero rendere restful le API esposte
* voto
	* [ ] template scrutinio