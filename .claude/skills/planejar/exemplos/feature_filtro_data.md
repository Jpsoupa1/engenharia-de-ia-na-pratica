<!-- Conceito: exemplo de plano aprovável. É a feature do exercício 5; o código NÃO está implementado no repositório. -->

# Plano: filtro por data na lista de tarefas

**Esteira:** padrão  ·  **Estimativa:** 1 hora

## Objetivo
Permitir listar só as tarefas dentro de um intervalo de datas, com início e fim opcionais.

## Arquivos afetados
* `exemplo/src/listar.ts`: nova função `filtrarPorData`.
* `exemplo/test/listar.test.ts`: testes da nova função.
* `exemplo/README.md`: marcar a feature como feita.

## Passos
1. Escrever os testes dos critérios abaixo (vão falhar).
2. Implementar `filtrarPorData(tarefas, { de?, ate? })` reaproveitando `listar()` para manter a ordem.
3. Validar `de` e `ate` no formato AAAA-MM-DD; lançar erro claro se inválidos ou se `de > ate`.
4. Rodar `npm run verificar` em `exemplo/`.

## Critérios de aceite
* [ ] Com `de` e `ate`, devolve só tarefas com `de <= data <= ate` (limites inclusivos).
* [ ] Só `de`: tudo a partir da data. Só `ate`: tudo até a data. Nenhum dos dois: igual a `listar()`.
* [ ] Resultado na mesma ordem de `listar()`.
* [ ] Não altera a lista original.
* [ ] Data fora do formato AAAA-MM-DD lança erro com a data na mensagem.
* [ ] `de` depois de `ate` lança erro.

## Testes
* "inclui os limites do intervalo": tarefas exatamente em `de` e em `ate` aparecem.
* "só de" e "só ate": intervalos abertos.
* "sem filtro devolve tudo ordenado".
* "recusa data inválida" e "recusa intervalo invertido": casos negados.

## Riscos
* Comparar datas como texto só funciona no formato ISO: por isso a validação do passo 3.

## Fora do escopo
* Fuso horário e hora do dia.
* Combinar filtro por data com filtro por status numa função só.
* Mudar o formato do campo `data`.
