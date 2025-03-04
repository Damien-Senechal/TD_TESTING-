## commande pour myenv
```bash
myenv\Scripts\activate
```


## commande pour lancer les testes de factires dans l'env
```bash
pytest BDD2/tests/test_facture.py
```

## Commande pour appliquer les testes de factures 

```bash
myenv/Scripts/python.exe -m unittest discover -s BDD2/tests -p "test_*.py"
```