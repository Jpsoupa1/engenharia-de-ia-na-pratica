<!-- Conceito: LLM como juiz, uma rubrica objetiva com notas descritas e saída em JSON. -->
# Rubrica para LLM como juiz

Use o juiz para o que o código não mede. O que dá para checar com teste, cheque com teste.

## Entrada do juiz

* O pedido original e os critérios de aceite.
* O diff produzido.
* O resultado dos testes, lint e typecheck.

Não passe o raciocínio do gerador. Dê só o que um revisor humano veria.

## Critérios, de 1 a 5

### 1. Cumprimento dos critérios de aceite
* **1:** não cumpre a maioria.
* **2:** cumpre menos da metade.
* **3:** cumpre a maioria, falha em um critério importante.
* **4:** cumpre todos, com uma falha menor.
* **5:** cumpre todos, com evidência (teste ou saída).

### 2. Escopo
* **1:** mexeu em muitos arquivos sem relação com o pedido.
* **2:** mudanças extras relevantes, como dependência nova.
* **3:** uma mudança extra pequena.
* **4:** só o pedido, com um ajuste colateral justificável.
* **5:** só o que foi pedido, nada a mais.

### 3. Testes
* **1:** sem testes, ou testes removidos.
* **2:** testes só do caminho feliz.
* **3:** cobre o principal, falta o caso negado.
* **4:** cobre o principal e o negado.
* **5:** cobre principal, negado e bordas, e o teste falharia sem a mudança.

### 4. Clareza e convenções
* **1:** ilegível ou fora das convenções do projeto.
* **2:** vários desvios das convenções.
* **3:** legível, com desvios pequenos.
* **4:** segue as convenções, nomes claros.
* **5:** segue as convenções e é simples de manter.

### 5. Segurança
* **1:** introduz falha clara, como segredo no código ou entrada sem validar.
* **2:** deixa risco evidente sem tratar.
* **3:** sem falha, mas sem validar o que deveria.
* **4:** valida e nega por padrão.
* **5:** valida, nega por padrão e testa o caso negado.

## Formato de saída

O juiz responde só com JSON:

```json
{
  "caso": "filtro_por_data",
  "notas": {
    "criterios_de_aceite": 4,
    "escopo": 5,
    "testes": 3,
    "clareza": 4,
    "seguranca": 4
  },
  "justificativas": {
    "criterios_de_aceite": "Cumpre os quatro casos do filtro. Falta o teste do intervalo vazio.",
    "escopo": "Só src/listar.ts e o teste foram alterados.",
    "testes": "Não há teste do caso em que de é maior que ate.",
    "clareza": "Nomes claros, segue o biome.",
    "seguranca": "Não aplica entrada externa, sem risco novo."
  },
  "aprovado": true
}
```

`aprovado` é verdadeiro quando nenhuma nota é menor que 3 e a média é pelo menos 4.

## Cuidados

* **Juiz diferente do gerador.** Um modelo tende a gostar do próprio texto. Se o Sonnet gerou, julgue com outro modelo.
* **Calibre com notas humanas.** Pontue de 10 a 20 casos você mesmo, rode o juiz e compare. Se discordam muito, reescreva a rubrica até as notas se aproximarem.
* **Notas descritas, não adjetivos.** "Bom" e "ruim" não ajudam. A descrição de cada nota precisa ser verificável.
* **Peça a justificativa antes da nota**, ou junto, para o juiz não chutar.
* **Cuidado com tamanho.** Juízes tendem a favorecer respostas mais longas. Penalize escopo extra.
* **Reveja de tempos em tempos.** Se o juiz e a pessoa passarem a divergir, recalibre.
* **Não é o portão final.** Em risco alto, quem aprova é gente.

**Próximo problema:** como medir o tempo de cada execução. Veja a [observabilidade](../observabilidade/README.md).
