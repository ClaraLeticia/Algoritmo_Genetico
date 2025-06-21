import random

class AlgoritmoGenetico:
    def __init__(self, aptidao, faixa_operacao, precisao, num_individuos, num_geracoes, taxa_mutacao):
        self.aptidao = aptidao
        self.faixa_operacao = faixa_operacao
        self.precisao = precisao
        self.num_individuos = num_individuos
        self.num_geracoes = num_geracoes
        self.taxa_mutacao = taxa_mutacao

        # Calcula o número de bits necessários para cada variável (x e y)
        self.cromossomos = int((faixa_operacao[1] - faixa_operacao[0]) / precisao).bit_length()
        self.genes = self.cromossomos * 2  # metade para x e metade para y

    def binario_para_real(self, bits):
        # Divide os bits igualmente para x e y
        bits_x = bits[:self.cromossomos]
        bits_y = bits[self.cromossomos:]

        # Converte os bits para string
        bits_x_str = ''.join(str(bit) for bit in bits_x)
        bits_y_str = ''.join(str(bit) for bit in bits_y)

        # Converte para inteiro
        int_x = int(bits_x_str, 2)
        int_y = int(bits_y_str, 2)

        # Normaliza para o intervalo desejado
        max_int = (1 << self.cromossomos) - 1  # 2^cromossomos - 1
        decimal_x = self.faixa_operacao[0] + (self.faixa_operacao[1] - self.faixa_operacao[0]) * int_x / max_int
        decimal_y = self.faixa_operacao[0] + (self.faixa_operacao[1] - self.faixa_operacao[0]) * int_y / max_int

        return decimal_x, decimal_y
        
    def gerar_individuo(self):
        return [random.randint(0, 1) for _ in range(self.genes)]
    
    def gerar_populacao(self):
        return [self.gerar_individuo() for _ in range(self.num_individuos)]
    
    def calcular_aptidao(self, populacao):
        fitness_populacao = {}
        for individuo in populacao:
            x, y = self.binario_para_real(individuo)
            fitness_populacao[tuple(individuo)] = self.aptidao(x, y)
        return fitness_populacao

    def cruzar(self, pai1, pai2):
        ponto_cruzamento = random.randint(1, self.genes - 1)
        filho1 = pai1[:ponto_cruzamento] + pai2[ponto_cruzamento:]
        filho2 = pai2[:ponto_cruzamento] + pai1[ponto_cruzamento:]
        return filho1, filho2
    
    def mutar(self, individuo):
        for i in range(len(individuo)):
            if random.random() < self.taxa_mutacao:
                individuo[i] = 1 - individuo[i]
        return individuo

    def selecao_roleta(self, populacao, fitness_populacao):
        total_fitness = sum(fitness_populacao.values())
        if total_fitness == 0:
            return random.sample(populacao, 2)
        
        roleta = []
        acumulado = 0
        for ind in populacao:
            prob = fitness_populacao[tuple(ind)] / total_fitness
            acumulado += prob
            roleta.append(acumulado)
        
        pais = []
        for _ in range(2):
            sorteio = random.random()
            for i, prob in enumerate(roleta):
                if sorteio <= prob:
                    pais.append(populacao[i])
                    break
        return pais[0], pais[1]

    def run(self):
        populacao = self.gerar_populacao()
        melhor_fitness_global = float('-inf')
        melhor_individuo_global = None
    
        for geracao in range(self.num_geracoes):
            fitness_pop = self.calcular_aptidao(populacao)
            
            # Encontra o melhor indivíduo da geração atual
            melhor_individuo = max(fitness_pop, key=fitness_pop.get)
            melhor_fitness = fitness_pop[melhor_individuo]
            
            # Atualiza o melhor global
            if melhor_fitness > melhor_fitness_global:
                melhor_fitness_global = melhor_fitness
                melhor_individuo_global = melhor_individuo
            
            # Elitismo: preserva os melhores indivíduos
            nova_populacao = []
            if melhor_individuo_global is not None:
                nova_populacao.append(list(melhor_individuo_global))
            
            while len(nova_populacao) < self.num_individuos:
                pai1, pai2 = self.selecao_roleta(populacao, fitness_pop)
                filho1, filho2 = self.cruzar(pai1, pai2)
                filho1 = self.mutar(filho1)
                nova_populacao.append(filho1)
                if len(nova_populacao) < self.num_individuos:
                    filho2 = self.mutar(filho2)
                    nova_populacao.append(filho2)
    
            populacao = nova_populacao
            
            x, y = self.binario_para_real(melhor_individuo)
            print(f"Geração {geracao+1}: Melhor indivíduo = f({x:.5f}, {y:.5f}) = {melhor_fitness:.5f}")
    
        print("\nAlgoritmo finalizado.")
        x, y = self.binario_para_real(melhor_individuo_global)
        print(f"Melhor solução encontrada: f({x:.5f}, {y:.5f}) = {melhor_fitness_global:.5f}")