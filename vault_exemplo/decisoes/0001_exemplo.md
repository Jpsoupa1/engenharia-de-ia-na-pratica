---
tipo: adr
numero: 1
titulo: Lista de tarefas em memória no projeto de exemplo
status: aceita
data: 2026-11-16
projeto: exemplo
tags: [adr, exemplo]
---
<!-- Conceito: ADR, registro curto de uma decisão com contexto, alternativas e consequências. -->
# 0001. Lista de tarefas em memória no projeto de exemplo

## Contexto

O projeto `exemplo/` existe para treinar o uso de agentes, não para virar produto. O participante precisa rodar tudo em minutos, sem instalar banco nem configurar credenciais.

## Decisão

As tarefas ficam em memória, em um array no código, com uma lista inicial de exemplo.

## Alternativas

* **Arquivo JSON:** persiste, mas traz leitura e escrita de disco e mais casos de erro para um exemplo curto.
* **Banco de dados:** realista, mas exige instalação, credenciais e migrações. Foge do objetivo.

## Consequências

* Os testes são rápidos e determinísticos.
* Nada persiste entre execuções. Isso é aceitável aqui.
* Mover para um banco depois é uma decisão nova e pede outro ADR.
* O exemplo não deve ser copiado como arquitetura de produção.
