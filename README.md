# CoVePoBot v. 0.1
================

Overview
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

Esempi
--------
* Gli url riportati di seguito possono essere testati sostituendo "DOMINIO" con "effedici.pythonanywhere.com"
* Negli esempi di seguito è stata usata la seguente convenzione:
  * XXX = alfanumerico, è il nome della sessione (influirà sugli url per la conversione)
  * YYY = numerico, è il numero di otp da attivare
  * ZZZ = alfanumerico, è la password di amministrazione fornita da CoVePoBot alla creazione della nuova sessione di voto
  * OOO = numerico, è l'OTP da convertire in secret
  * SSS = alfanumerico, è il secret ottenuto dalla conversione dell'OTP

Amministrazione
--------
### Creazione di una nuova sessione di voto ###
(es: un'assemblea)
* La CoVePo può attivare una nuova sessione di voto invocando l'url
  > http://DOMINIO/CoVePoBot/session?id=XXX&num=YYY
* esempio di risposta:
  > Aggiunta la nuova sessione XXX. Usa come password per la gestione: ZZZ
  > Gli otp disponibili sono: 123456,234567,345678,456789,567890

### Recupero della lista di "secret" attivati ###
* La CoVePo può recuperare la lista dei secret attivati dagli utenti.
  > http://DOMINIO/CoVePoBot/XXX/secrets?password=ZZZ
* esempio di risposta:
  >as5d64fr97,b69b91a53a
* Un secret si attiva convertendo l'OTP all'opportuno URL
* Da un secret non è possibile risalite all'OTP convertito

### Recupero della lista di OTP non convertiti ancora dagli utenti ###
* La CoVePo può recuperare la lista degli OTP non ancora attivati dagli utenti.
  > http://DOMINIO/CoVePoBot/XXX/otps/?password=ZZZ
* esempio di risposta:
  > 234567,345678,456789,567890

### Aggiunta di ulteriori OTP alla sessione di voto ###
* La CoVePo può aggiungere nuovi OTP alla sessione di voto.
  > http://DOMINIO/CoVePoBot/XXX/additionalotp/?password=ZZZ&num=YYY
* esempio di risposta:
  > La sessione XXX è stata aggiornata.
  > I nuovi otp disponibili sono: 098765,987654,876543

### Rimozione di un secret ###
* La CoVePo può annullare un secret a partire dal relativo OTP.
  > http://DOMINIO/CoVePoBot/XXX/secret/OOO/?password=ZZZ
* esempio di risposta:
  > Secret disabilitato

  /CoVePoBot/<vote_id>/secret/<secret>

Come si attiva l’OTP
--------
* L'utente dovrà chiamare un URL da browser come il seguente (sostituire OOO con l'OTP)
  > http://DOMINIO/CoVePoBot/XXX/otp/OOO
* esempio di risposta:
  > Il tuo codice è SSS e ti servirà per votare alla XXX.
  > Attenzione! Non sarà possibile riprodurlo nuovamente. Perciò conservalo accuratamente e non perderlo
* Si suggerisce che la CoVePo fornisca direttamente il link completo poiché non tutti gli utenti sono in grado di costruire un URL.

Piattaforma
--------
* L'applicativo è scritto in Python con Framework Flask.
* Al momento non sono previste versioni specifiche per ogni piattaforma.
* Una istanza d'esempio è disponibile e funzionante al dominio
  > effedici.pythonanywhere.com

Sviluppi futuri
--------
* migliorare la guida
* prevedere il salvataggio dei dati non in sessione (db o file in drive)
* fornire la lista degli OTP sottoforma di URL già pronti