"""
Avaliação Prática N1 - Inteligência Artificial
IFCE Campus Tauá - Análise e Desenvolvimento de Sistemas (ADS)
Dupla: Guilherme Alves dos Santos e Guilherme Monteiro de Sousa
Tema C - Controlador de Velocidade de Ventilador
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import warnings
import os

# Ignorando os warnings conforme solicitado
warnings.filterwarnings("ignore")

# Criando a pasta imagens/ automaticamente
os.makedirs('imagens', exist_ok=True)

# ==============================================================================
# 1. DEFINIÇÃO DAS VARIÁVEIS LINGUÍSTICAS E UNIVERSOS DE DISCURSO
# ==============================================================================

# Temperatura em graus Celsius (0 a 40 graus)
temperatura = ctrl.Antecedent(np.arange(0, 41, 1), 'temperatura')

# Ocupação da sala em porcentagem (0% a 100%)
ocupacao = ctrl.Antecedent(np.arange(0, 101, 1), 'ocupacao')

# Velocidade do ventilador em porcentagem da potência (0% a 100%)
velocidade = ctrl.Consequent(np.arange(0, 101, 1), 'velocidade')


# ==============================================================================
# 2. FUNÇÕES DE PERTINÊNCIA (MEMBERSHIP FUNCTIONS)
# ==============================================================================

# Temperatura
temperatura['baixa'] = fuzz.trapmf(temperatura.universe, [0, 0, 18, 22])
temperatura['agradavel'] = fuzz.trimf(temperatura.universe, [18, 24, 30])
temperatura['alta'] = fuzz.trapmf(temperatura.universe, [26, 32, 40, 40])

# Ocupação
ocupacao['vazia'] = fuzz.trapmf(ocupacao.universe, [0, 0, 20, 40])
ocupacao['media'] = fuzz.trimf(ocupacao.universe, [30, 50, 70])
ocupacao['cheia'] = fuzz.trapmf(ocupacao.universe, [60, 80, 100, 100])

# Velocidade do Ventilador
velocidade['desligado'] = fuzz.trimf(velocidade.universe, [0, 0, 20])
velocidade['baixa'] = fuzz.trimf(velocidade.universe, [10, 30, 50])
velocidade['media'] = fuzz.trimf(velocidade.universe, [40, 60, 80])
velocidade['alta'] = fuzz.trapmf(velocidade.universe, [70, 90, 100, 100])


# --- SALVANDO OS GRÁFICOS INICIAIS ---
# Entrada 1
temperatura.view()
plt.savefig('imagens/pertinencia_entrada1.png')
plt.close() # Limpa a memória para o próximo gráfico

# Entrada 2
ocupacao.view()
plt.savefig('imagens/pertinencia_entrada2.png')
plt.close()

# Saída (O GRÁFICO QUE FALTAVA COM O NOME CORRETO)
velocidade.view()
plt.savefig('imagens/pertinencia_saida.png')
plt.close()


# ==============================================================================
# 3. BASE DE REGRAS FUZZY
# ==============================================================================

regra1 = ctrl.Rule(temperatura['baixa'] & ocupacao['vazia'], velocidade['desligado'])
regra2 = ctrl.Rule(temperatura['baixa'] & ocupacao['media'], velocidade['desligado'])
regra3 = ctrl.Rule(temperatura['baixa'] & ocupacao['cheia'], velocidade['baixa']) 

regra4 = ctrl.Rule(temperatura['agradavel'] & ocupacao['vazia'], velocidade['desligado'])
regra5 = ctrl.Rule(temperatura['agradavel'] & ocupacao['media'], velocidade['baixa'])
regra6 = ctrl.Rule(temperatura['agradavel'] & ocupacao['cheia'], velocidade['media'])

regra7 = ctrl.Rule(temperatura['alta'] & ocupacao['vazia'], velocidade['baixa']) 
regra8 = ctrl.Rule(temperatura['alta'] & ocupacao['media'], velocidade['media'])
regra9 = ctrl.Rule(temperatura['alta'] & ocupacao['cheia'], velocidade['alta']) 


# ==============================================================================
# 4. INFERÊNCIA (MAMDANI) E DEFUZZIFICAÇÃO (CENTROIDE)
# ==============================================================================

controle_ventilador = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8, regra9])
simulador = ctrl.ControlSystemSimulation(controle_ventilador)


# ==============================================================================
# 5. TESTES E GERAÇÃO DO GRÁFICO FINAL DE SAÍDA
# ==============================================================================

cenarios = [
    {"descricao": "1. Sala vazia e fria", "temp": 15, "ocup": 10},
    {"descricao": "2. Sala com ocupação média e temp. agradável", "temp": 24, "ocup": 50},
    {"descricao": "3. Sala cheia e muito quente", "temp": 36, "ocup": 95},
    {"descricao": "4. Sala vazia, mas muito quente (insolação)", "temp": 35, "ocup": 10},
    {"descricao": "5. Sala cheia, mas fria (inverno intenso)", "temp": 12, "ocup": 90}
]

print("="*50)
print("=== RESULTADOS DOS TESTES FUZZY (TEMA C) ===")
print("="*50)

for i, cenario in enumerate(cenarios):
    simulador.input['temperatura'] = cenario['temp']
    simulador.input['ocupacao'] = cenario['ocup']
    simulador.compute()
    resultado = simulador.output['velocidade']
    
    print(f"\n{cenario['descricao']}")
    print(f"   [Entradas] -> Temperatura: {cenario['temp']}°C | Ocupação: {cenario['ocup']}%")
    print(f"   [Saída]    -> Velocidade do Ventilador: {resultado:.2f}%")
    
    # Gerando o gráfico preenchido do Centroide para o cenário extremo (3)
    if i == 2:
        velocidade.view(sim=simulador)
        plt.title("Defuzzificação (Centroide) - Sala cheia e muito quente")
        plt.savefig('imagens/saida_fuzzy.png')
        plt.close()
        
print("\n" + "="*50)
print("Pronto! Agora você tem 4 imagens separadas na pasta 'imagens/'.")