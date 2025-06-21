from algoritmo_genetico import AlgoritmoGenetico
import math

# Definindo a função de aptidão (quanto menor, melhor)
def funcao_aptidao(x, y):
    # Exemplo: minimizar |e^(-x) - y^2 + 1| + 1e-4
    return abs(math.exp(-x) - y**2 + 1) + 1e-4

if __name__ == "__main__":
    ag = AlgoritmoGenetico(
        aptidao=funcao_aptidao,
        faixa_operacao=(-10, 10),
        precisao=0.005,
        num_individuos=100,
        num_geracoes=100,
        taxa_mutacao=0.05
    )

    ag.run()
