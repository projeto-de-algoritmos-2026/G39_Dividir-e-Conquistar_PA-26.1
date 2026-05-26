# StatRank
 
Ferramenta para encontrar o **k-ésimo menor valor** em grandes datasets usando o algoritmo **Mediana das Medianas**.
 
Desenvolvido como trabalho prático da disciplina **Projeto de Algoritmos** — módulo Dividir e Conquistar.
 
---
 
## Problema real
 
Em sistemas que processam grandes volumes de dados (folhas de pagamento, resultados de exames, transações financeiras), calcular percentis de forma eficiente é essencial. Ordenar o dataset inteiro é desnecessário: só precisamos do **k-ésimo menor elemento**.
 
---
 
## Motivação
 
O Quickselect resolve o problema em O(n) na média, mas pode degradar para O(n²) com entradas adversas. A Mediana das Medianas garante O(n) mesmo no pior caso, usando um pivô criterioso: divide o array em grupos de 5, calcula a mediana de cada grupo e usa a mediana dessas medianas como pivô — garantindo que pelo menos 30% dos elementos ficam em cada lado da partição.
 
---
 
## Autores
 
- Eduardo de Almeida Morais
 