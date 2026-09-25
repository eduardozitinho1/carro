# Como jogar

O `carro` é um jogo de gerenciamento baseado em viagens, trabalhos, dinheiro, upgrades e risco.

Você não precisa controlar o carro em tempo real. A direção é representada pelas decisões que você toma no terminal.

## Menu principal

O jogo possui atualmente estas opções:

```text
1. Ver status do carro
2. Acelerar
3. Desacelerar
4. Parar
5. Viajar
6. Trabalhar
7. Ver status do jogador
8. Upgrades
9. Abastecer
s. Sair
```

## Status do carro

O status mostra informações importantes sobre seu veículo, incluindo:

- localização atual;
- velocidade atual;
- velocidade máxima;
- combustível;
- airbags;
- upgrades de velocidade.

Use essa informação para decidir quando viajar, abastecer ou comprar melhorias.

## Velocidade

A velocidade máxima inicial é de:

**150 km/h**

A velocidade influencia diretamente o tempo da viagem.

Quanto maior a velocidade, menor será o tempo necessário para percorrer a mesma distância.

Você pode aumentar a velocidade máxima comprando upgrades de velocidade.

Cada upgrade aumenta a velocidade máxima em:

**25 km/h**

## Viagens

Para viajar, o carro precisa estar em movimento.

O jogo calcula a distância entre o local atual e o destino.

Durante a viagem, o combustível é consumido e eventos aleatórios podem acontecer.

Uma viagem pode:

- ser concluída normalmente;
- sofrer atrasos;
- ser interrompida por um acidente;
- ser interrompida por uma ocorrência de imprudência;
- resultar em prisão.

Quando uma viagem é interrompida, você precisa refazê-la.

## Combustível

O carro possui uma quantidade limitada de combustível.

Uma viagem consome combustível proporcionalmente à distância percorrida.

Se não houver combustível suficiente para completar uma viagem, ela não poderá ser iniciada.

Use a opção de abastecimento para recuperar combustível.

## Trabalhos

Trabalhos são a principal fonte de dinheiro do jogador.

Cada estado possui um trabalho associado.

Alguns trabalhos exigem determinada qualidade do jogador e possuem uma chance de aceitação.

Consulte [Trabalhos](jobs.md) para entender o sistema.

## Dinheiro

Você começa com:

**R$50,00**

O dinheiro pode ser usado para comprar melhorias e outros recursos do jogo.

Seu objetivo é aumentar seu patrimônio através das entregas.

## Upgrades

Existem três tipos principais de melhorias:

- airbags;
- advogados;
- velocidade.

Cada melhoria possui um custo próprio.

Consulte [Upgrades](upgrades.md).

## Risco

Viajar não é completamente seguro.

Eventos aleatórios são parte central do jogo.

Você precisa equilibrar:

- velocidade;
- dinheiro;
- upgrades;
- combustível;
- risco.

Consulte [Eventos](events.md) para conhecer os acontecimentos que podem ocorrer durante uma viagem.
