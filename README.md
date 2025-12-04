# Projeto: Sistema Fuzzy para Controle de Ventilação (Tema C)

## 👥 Identificação da Dupla
* **Aluno 1:** [Guilherme Alves dos Santos] 
* **Aluno 2:** [Guilherme Monteiro de Sousa] 

## 🎯 Tema Escolhido
**Tema C – Controlador de Ventilação**

## 📝 Descrição Inicial do Problema
O objetivo deste projeto é desenvolver um sistema de controle inteligente para a velocidade de um ventilador em um ambiente fechado. Diferente de sistemas tradicionais (ligado/desligado), este sistema ajustará a rotação do ventilador de forma gradual e otimizada, baseando-se em duas variáveis principais: a **temperatura ambiente** e a **taxa de ocupação** da sala. Isso visa garantir o conforto térmico e a eficiência energética.

## 📅 Planejamento Inicial do Projeto

### 1. Definição das Variáveis Linguísticas
* **Entrada 1:** Temperatura (Unidade: Graus Celsius °C).
    * *Universos de Discurso (Sugestão):* 0°C a 40°C.
* **Entrada 2:** Taxa de Ocupação (Unidade: Porcentagem % ou quantidade de pessoas).
    * *Universos de Discurso (Sugestão):* 0% a 100%.
* **Saída:** Velocidade do Ventilador (Unidade: % da potência máxima).
    * *Universos de Discurso:* 0% a 100%.

### 2. Esboço das Funções de Pertinência (Membership Functions)
Serão utilizados conjuntos fuzzy triangulares e trapezoidais para cobrir as faixas de valores:
* **Temperatura:** Baixa, Agradável, Alta.
* **Ocupação:** Vazia, Média, Cheia.
* **Velocidade:** Desligado, Baixa, Média, Alta.

### 3. Estrutura da Base de Regras
As regras seguirão a lógica "SE... ENTÃO". Exemplo preliminar:
* *SE* a temperatura é Alta *E* a ocupação é Cheia, *ENTÃO* a velocidade é Alta.
* *SE* a temperatura é Baixa, *ENTÃO* a velocidade é Desligado (independente da ocupação).

### 4. Método de Inferência
Será utilizado o método de **Mamdani** (Min-Max), que é intuitivo e amplamente aceito para sistemas de controle baseados em conhecimento especialista.

### 5. Método de Defuzzificação
Para converter a saída fuzzy em um valor numérico real (crisp) para o motor do ventilador, será utilizado o método do **Centroide (Centro de Gravidade)**.

### 6. Cenários de Teste
O sistema será validado com cenários extremos e medianos, por exemplo:
* Sala vazia e fria (Esperado: Ventilador desligado).
* Sala cheia e muito quente (Esperado: Velocidade máxima).
* Sala com ocupação média e temperatura agradável (Esperado: Velocidade baixa/média para manutenção do conforto).
