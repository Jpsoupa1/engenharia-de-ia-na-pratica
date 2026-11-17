<!--
  Este CLAUDE.md é RUIM DE PROPÓSITO.
  Serve ao exercício 2: encontre o que repete o código, o que é vago, o que é histórico velho,
  o que se contradiz, o que deveria ser skill e o que deveria ser hook.
  Não copie este arquivo para um projeto de verdade.
-->
# CLAUDE.md do projeto de tarefas

## Sobre o projeto
Este projeto é uma aplicação de lista de tarefas escrita em TypeScript.
O projeto usa TypeScript.
O código fica na pasta src.
Os testes ficam na pasta test.
O arquivo package.json tem as dependências.
O arquivo tsconfig.json tem a configuração do TypeScript.
O arquivo biome.json tem a configuração do biome.
A pasta node_modules tem as dependências instaladas.

## Estrutura
* src/tarefas.ts tem o tipo Tarefa e a função criarTarefa.
* src/listar.ts tem as funções listar e filtrarPorStatus.
* test/listar.test.ts tem os testes de listar.
* O tipo Tarefa tem id, titulo, status e data.
* O status pode ser pendente, fazendo ou feita.
* A data é uma string.

## Regras de código
* Escreva código limpo.
* Faça um bom trabalho.
* Seja cuidadoso.
* Use boas práticas.
* Escreva código bonito e fácil de entender.
* Não escreva bugs.
* Sempre pense bem antes de agir.
* Escreva testes bons.
* O código deve ser performático.
* Use nomes adequados.

## Estilo
* Use sempre ponto e vírgula no fim das linhas.
* Nunca use ponto e vírgula no fim das linhas.
* Use aspas duplas.
* Use aspas simples nas strings curtas.
* Indente com 2 espaços.
* Indente com tabs.
* Sempre comente todas as funções.
* Não escreva comentários, o código deve falar por si.

## Histórico de decisões
* Em 2021 usamos Jest, depois trocamos para Mocha, depois voltamos para Jest.
* Em 2022 tentamos usar Redux, mas desistimos porque era pesado.
* Em 2022 o Carlos queria usar MongoDB, mas escolhemos arquivo JSON.
* Em 2023 migramos de JavaScript para TypeScript, a migração terminou em março.
* Em 2023 usamos ESLint e Prettier, e depois trocamos pelo biome.
* A versão 1 da API foi descontinuada. Ainda existe um comentário sobre ela em src/listar.ts.
* Antes tínhamos um servidor Express, mas ele foi removido.
* A pasta legado foi apagada, mas talvez volte.

## Como fazer o release
Quando for fazer um release, siga estes passos com atenção.
1. Confira se a branch está atualizada com a main.
2. Rode npm install para garantir as dependências.
3. Rode npm run lint e corrija os erros.
4. Rode npm run typecheck e corrija os erros.
5. Rode npm test e confira que passa.
6. Atualize a versão no package.json seguindo o semver.
7. Se for correção, aumente o patch.
8. Se for funcionalidade, aumente o minor.
9. Se quebrar compatibilidade, aumente o major.
10. Atualize o CHANGELOG com a data de hoje.
11. Liste cada PR mergeado desde o último release no CHANGELOG.
12. Agrupe os itens do CHANGELOG em Adicionado, Corrigido e Removido.
13. Faça o commit com a mensagem "release: vX.Y.Z".
14. Crie a tag com o mesmo número.
15. Envie a tag para o repositório.
16. Abra o PR de release.
17. Peça revisão a duas pessoas.
18. Depois do merge, confira se a pipeline publicou.
19. Avise o time no canal.
20. Se algo falhar, reverta o commit e avise o time.

## Segurança
* Nunca leia o arquivo .env.
* Nunca faça push forçado.
* Nunca execute rm -rf fora do projeto.
* Nunca faça deploy de produção sem aprovação.
* Sempre confira os comandos antes de rodar.
* Se precisar ler o .env para depurar, pode ler.

## Testes
* Sempre rode os testes antes de terminar.
* Não precisa rodar os testes em mudanças pequenas.
* Rode os testes com npm test.
* Rode os testes com npx vitest.
* Escreva testes para tudo.
* Não perca tempo com testes de coisas simples.

## Commits
* Faça commits pequenos.
* Faça um commit só no fim da tarefa.
* A mensagem do commit deve ser clara.
* Use o padrão de commits convencionais.
* Não precisa seguir nenhum padrão de mensagem.

## Comunicação
* Seja educado.
* Explique tudo o que fizer, em detalhes.
* Seja breve.
* Sempre peça confirmação antes de qualquer ação.
* Não fique pedindo confirmação o tempo todo.

## Observações gerais
* Este arquivo foi começado em 2021 e já foi editado por muita gente.
* Se tiver dúvida, pergunte.
* Não invente coisas.
* Lembre-se de que o projeto é importante.
* Tenha atenção aos detalhes.
* TODO: reescrever este arquivo.
* TODO: ver se ainda precisamos da pasta legado.
* TODO: documentar a API.
