from teste_class import Sinal

## carregando o sinal:
filename="ang1.wav"
# atribuindo a o objeto à classe Sinal
a=Sinal(filename)
# método carrega sinal
a.carrega()
## método calcula a intensidade
a.getIntensity()
## printando o valor médio da intensidade
print(a.meanIntensity)

## tomando o CPPS
a.getCPPS()
print("O valor do CPPS foi: ",a.cpps)