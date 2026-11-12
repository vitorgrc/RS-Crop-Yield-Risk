# Guia de leitura do painel — Agricultura no RS

Texto pronto para a página **Guia de leitura** do Power BI e para o artigo. Escrito para quem não é especialista e para quem usa os números em decisões de negócio.

## Para que serve o painel

Mostra **onde e quando** as safras de soja, milho, arroz e trigo do Rio Grande do Sul renderam menos do que o esperado e **quanto do clima** (chuva, temperatura, dias secos) acompanha essas quebras. Foi pensado para quem decide sobre crédito, seguro, assistência técnica ou política agrícola.

## Perguntas que o painel responde

- Quanto o RS (ou uma região) produziu, em que área e com qual rendimento?
- A safra do ano foi boa ou ruim **para o que se esperava** (e não apenas comparada ao ano anterior)?
- Quais culturas e quais municípios têm rendimento mais instável?
- Qual foi o pior ano já registrado e quão grave foi?
- A chuva do ciclo acompanha o desempenho da lavoura?

## O que o painel não responde

- **Causa** das quebras: mostra coincidências, não provas.
- **Previsão** da próxima safra.
- Risco de um **produtor individual**: o dado é médio por município.
- Rentabilidade: não há custos nem preços recebidos.

## Como ler as cores e os termos

- **Tendência**: o rendimento que se esperava para o ano, considerando que a lavoura evolui com o tempo (melhores sementes, manejo).
- **Desvio**: quanto o rendimento real ficou acima (verde) ou abaixo (vermelho) dessa expectativa.
- **Anomalia**: quanto o ano fugiu do normal da região (chuva em %, temperatura em °C).

## Dicionário de indicadores

Origem: **Extraída** = vem direto da fonte; **Calculada** = construída neste projeto.

### Página Panorama

**Produção (t)** (Extraída)

- **O que é:** Quantidade colhida no ano, para a cultura e a região selecionadas.
- **Como é calculado:** Soma da produção dos municípios (IBGE, Pesquisa Agrícola Municipal – PAM).
- **Como ler:** Compare com os anos vizinhos no gráfico de safras: a série mostra se o ano foi de alta ou de queda.
- **Uso na decisão:** Dimensiona a oferta local: armazenagem, logística, volume de crédito e de insumos.
- **Cuidado:** Produção pode cair só porque a área diminuiu. Para saber se a lavoura rendeu menos, olhe o rendimento.

**Área colhida (ha)** (Extraída)

- **O que é:** Área efetivamente colhida.
- **Como é calculado:** Soma da área dos municípios (IBGE/PAM).
- **Como ler:** Junto com a produção, mostra se a mudança veio de mais/menos área ou de mais/menos rendimento.
- **Uso na decisão:** Separa expansão de área de ganho de produtividade.
- **Cuidado:** Em anos de perda, a área colhida pode ser menor que a plantada.

**Rendimento (kg/ha)** (Calculada)

- **O que é:** Quanto se colhe por hectare (produtividade).
- **Como é calculado:** Produção (t) × 1.000 ÷ área colhida (ha). É a média do conjunto, ponderada pela área.
- **Como ler:** Quanto maior, melhor. Para soja, divida por 60 para obter sacas por hectare (2.093 kg/ha ≈ 35 sc/ha).
- **Uso na decisão:** Base para comparar regiões e anos e para estimar a capacidade de pagamento do produtor.
- **Cuidado:** É média: esconde a diferença entre produtores bons e ruins dentro da mesma região.

**Valor da produção (milhão R$)** (Calculada)

- **O que é:** Valor bruto da produção agrícola no ano.
- **Como é calculado:** Valor informado pelo IBGE (em mil R$) ÷ 1.000.
- **Como ler:** Mostra o peso econômico de cada cultura e região.
- **Uso na decisão:** Prioriza onde concentrar atenção, crédito e assistência técnica.
- **Cuidado:** Valores nominais, sem correção pela inflação: não compare anos muito distantes.

**Variação de produção** (Calculada)

- **O que é:** Mudança da produção em relação à safra anterior.
- **Como é calculado:** Produção do ano ÷ produção do ano anterior − 1.
- **Como ler:** Vermelho = safra menor que a anterior; azul = maior. Não é comparada com a tendência.
- **Uso na decisão:** Sinaliza rapidamente quebra ou recuperação.
- **Cuidado:** Compara só dois anos: depois de uma quebra forte, o ano seguinte mostra alta quase automática.

**Participação por região (%)** (Calculada)

- **O que é:** Peso de cada mesorregião na produção do RS, na cultura e no ano.
- **Como é calculado:** Produção da região ÷ produção total do RS.
- **Como ler:** Barra longa = produção concentrada naquela região.
- **Uso na decisão:** Mostra dependência geográfica: se poucas regiões respondem por quase tudo, um problema local afeta o estado.
- **Cuidado:** Participação em toneladas, não em valor.

**10 maiores produtores** (Calculada)

- **O que é:** Municípios com maior produção no ano.
- **Como é calculado:** Ordena os municípios por produção e mostra os 10 primeiros.
- **Como ler:** Barras em toneladas, de cima para baixo.
- **Uso na decisão:** Indica onde está o volume para ação comercial e assistência.
- **Cuidado:** Volume alto não significa estabilidade: consulte o CV na página de risco.

### Página Risco

**Tendência (kg/ha)** (Calculada)

- **O que é:** Rendimento esperado para o ano, considerando a evolução da lavoura entre 2000 e 2025.
- **Como é calculado:** Reta de tendência robusta (Theil–Sen): a inclinação é a mediana das inclinações entre todos os pares de anos. Inclinações do RS: soja +47, trigo +49, arroz +133, milho +169 kg/ha por ano.
- **Como ler:** Linha laranja no gráfico de rendimento. O rendimento do ano deve ser comparado com ela, e não com um valor fixo.
- **Uso na decisão:** Referência justa de produtividade: 3.000 kg/ha pode ser ruim em 2024 e ótimo em 2005.
- **Cuidado:** É uma estimativa estatística do passado, não uma previsão agronômica.

**Desvio vs tendência (%)** (Calculada)

- **O que é:** Quanto o rendimento do ano ficou acima ou abaixo do esperado.
- **Como é calculado:** Rendimento do ano ÷ tendência do ano − 1, em %.
- **Como ler:** −28 = 28% abaixo do esperado. Barras vermelhas = abaixo; verdes = acima.
- **Uso na decisão:** Mede a gravidade de uma quebra sem o efeito da evolução tecnológica.
- **Cuidado:** Depende de a tendência estar bem ajustada; é mais confiável em regiões e culturas com séries estáveis.

**Pior ano (desvio %)** (Calculada)

- **O que é:** A safra com maior queda frente à tendência em toda a série.
- **Como é calculado:** Menor valor do desvio vs tendência na série 2000–2025 e o ano em que ocorreu.
- **Como ler:** Ex.: 2005: −52 = o pior ano foi 2005, com rendimento 52% abaixo do esperado.
- **Uso na decisão:** Dá o pior cenário já observado, útil para testar a resistência de uma operação de crédito ou seguro.
- **Cuidado:** Mostra a gravidade, não a frequência. Use junto com o gráfico de desvio por ano.

**Variabilidade (CV, %)** (Calculada)

- **O que é:** Quanto o rendimento oscila de um ano para outro.
- **Como é calculado:** Desvio-padrão ÷ média × 100, por município e cultura, de 2010 a 2025 (mínimo de 10 anos de dados e área média de 500 ha).
- **Como ler:** Quanto maior, mais instável. Referência prática deste painel (não é norma): abaixo de 15% estável; 15–30% moderada; acima de 30% alta.
- **Uso na decisão:** Compara o risco entre culturas, regiões e municípios; apoia decisões sobre garantias, prazo e seguro.
- **Cuidado:** Calculado sobre o rendimento observado, que inclui o crescimento de longo prazo, então tende a superestimar um pouco a instabilidade.

**Municípios analisados** (Calculada)

- **O que é:** Número de municípios incluídos no cálculo de risco.
- **Como é calculado:** Municípios com pelo menos 10 anos de dados e área média de 500 ha na cultura.
- **Como ler:** Mostra a base da leitura.
- **Uso na decisão:** Poucos municípios significam leitura mais frágil para aquela região e cultura.
- **Cuidado:** Municípios pequenos na cultura ficam fora da análise.

**Média pior desvio (%)** (Calculada)

- **O que é:** Em média, qual foi a pior quebra dos municípios listados.
- **Como é calculado:** Pior desvio de cada município entre 2010 e 2025, resumido pela média no filtro.
- **Como ler:** Mais negativo = quebras mais fortes.
- **Uso na decisão:** Identifica os municípios de maior risco para acompanhamento.
- **Cuidado:** Um único ano muito ruim pesa muito; confira o CV.

### Página Clima

**Anomalia de chuva no ciclo (%)** (Calculada)

- **O que é:** Quanto choveu no ciclo da cultura, comparado com o normal da região.
- **Como é calculado:** (chuva do ciclo ÷ média 2001–2025 do mesmo ciclo e região − 1) × 100. Ciclos: soja nov–mar; milho e arroz out–mar; trigo jun–nov.
- **Como ler:** +22 = 22% mais chuva que o normal; −30 = 30% menos (ano seco).
- **Uso na decisão:** Aponta anos de seca ou de excesso de chuva e permite relacioná-los às quebras.
- **Cuidado:** Chuva modelada (ERA5) em um ponto por mesorregião; a chuva local pode ser bem diferente.

**Anomalia de temperatura (°C)** (Calculada)

- **O que é:** Diferença da temperatura média do ciclo para o normal da região.
- **Como é calculado:** Temperatura média do ciclo − média 2001–2025 do mesmo ciclo e região.
- **Como ler:** +0,35 = ciclo 0,35 °C mais quente que o normal. Variações de ±0,5 °C são comuns.
- **Uso na decisão:** Contexto para anos de calor ou frio fora do padrão.
- **Cuidado:** Sozinha, raramente explica a quebra; leia junto com chuva e dias secos.

**Dias secos no ciclo** (Calculada)

- **O que é:** Número de dias com menos de 1 mm de chuva no ciclo.
- **Como é calculado:** Contagem dos dias com chuva abaixo de 1 mm na série diária (ERA5/Open-Meteo).
- **Como ler:** Mais dias secos = maior risco de estiagem. Com várias regiões, o cartão mostra a média.
- **Uso na decisão:** Complementa a chuva total: a mesma chuva distribuída de formas diferentes tem efeitos diferentes.
- **Cuidado:** Dia seco não é, sozinho, dia de estresse: depende da fase da lavoura.

**Correlação chuva × desvio** (Calculada)

- **O que é:** Se os anos mais chuvosos coincidem com rendimento acima ou abaixo do esperado.
- **Como é calculado:** Coeficiente de Pearson entre anomalia de chuva e desvio do rendimento, nos anos da seleção.
- **Como ler:** Vai de −1 a +1. Perto de 0 = sem relação linear. 0,55 = relação positiva moderada: anos mais chuvosos tendem a render mais que o esperado.
- **Uso na decisão:** Mostra em quais culturas e regiões o clima mais pesa, o que orienta seguro e planejamento.
- **Cuidado:** Correlação não é causa. O sinal muda por cultura (todas as regiões, 2001–2025: soja +0,64; milho +0,56; trigo −0,53; arroz −0,28) e não capta o excesso de chuva, que também prejudica.

## Exemplo de leitura: soja em 2024

Segundo o painel, em 2024 o rendimento da soja do RS ficou cerca de 6% abaixo da tendência, o que parece pouco. Por região, a leitura muda: Metropolitana de Porto Alegre −28%, Sudeste −40%, Noroeste +7%. O estado como um todo esconde essas diferenças. Na Metropolitana, a chuva do ciclo ficou 22% acima da média, e o rendimento caiu: o oposto do padrão geral, em que mais chuva costuma acompanhar rendimento melhor. A base não permite dizer a causa, mas mostra que o clima não age de forma linear: falta e excesso de chuva podem coincidir com perdas.

## Fontes e limitações

**Fontes**

- Produção, área, rendimento e valor: IBGE, Pesquisa Agrícola Municipal (tabela 5457 do SIDRA), 2000–2025, municípios do RS.
- Clima: reanálise ERA5, via API Open-Meteo (dados modelados, não de estações).
- Limites dos municípios: base geográfica pública em TopoJSON.

**Limitações**

- O rendimento é a média de cada município. Dentro dele há produtores muito diferentes.
- O clima usa **um ponto de referência por mesorregião**, que pode não representar bem toda a região.
- As janelas de tempo diferem: séries de rendimento 2000–2025; CV 2010–2025; clima 2001–2025.
- O valor da produção é nominal (sem correção pela inflação).
- A correlação usa poucos anos (25 por região e cultura) e as regiões empilhadas não são independentes entre si.
- Um município (Pinto Bandeira) não aparece no mapa por falta do contorno na base geográfica usada.
- Dados mais recentes do IBGE podem ser revisados.

## Como usar esta documentação no Power BI

1. Importe `indicator_dictionary_pt.csv` (**Obter dados → Texto/CSV**, codificação UTF-8) sem relacioná-lo a outras tabelas.
2. Na nova página **Guia de leitura**, insira um visual **Tabela** com as colunas `indicador`, `o_que_e`, `como_e_calculado`, `como_ler`, `uso_na_decisao`, `cuidado`.
3. Em **Formatar visual → Valores**, ative a **quebra automática de texto**, defina largura de coluna e fonte 9–10 pt. Desative totais.
4. Opcional: insira uma segmentação de bloco com `pagina`, para o leitor filtrar o dicionário pela página do painel.
5. Nos blocos do topo (Para que serve, Como ler, Antes de decidir), use caixas de texto com o conteúdo das seções acima.
6. Em cada página, adicione um botão **Como ler** com ação de navegação para o Guia.
