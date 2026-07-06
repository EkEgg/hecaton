# Hecaton

Para executar:

```ps
python src/main.py --port <PORTA> --id <ID> --nodes <NODE_1> <NODE_2> <NODE_3> <...>
```

- <PORTA> é a porta em que você vai rodar no localhost.
- <ID> é o seu ID na sessão.
- <NODE_I> é um outro nó (não coloque você mesmo). Coloque todos os outros nós da rede no seguinte
  formato: <ID>=<HOST>:<PORTA>

Eis um exemplo:

```ps
python src/main.py --port 5000 --id 1 --nodes 0=100.20.80:5500 2=100.20.45:5800 3=100.40.10:1000
```
