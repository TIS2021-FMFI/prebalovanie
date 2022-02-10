# Readme - inštalácia

- aplikáca je implementovaná v Pythone, resp. v Djangu
- na spustenie je potrebné nainštalovať veci, ktoré sú uvedené v `requirements.txt`
- spustenie development servera sa vykonáva príkazom: `python manage.py runserver`
- spustenie production servera sa dá spraviť napr. podľa: [tohto návodu](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment) alebo [tohto návodu](https://docs.djangoproject.com/en/3.2/howto/deployment/)
- vytvorenie tasku na posielanie mailov cez windows cmd: `schtasks.exe /create /tn send-mails /sc daily  /st 18:00 /tr "curl '(adresa)/mails/send/'"`