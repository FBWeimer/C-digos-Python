import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def NN():
    neuronio=[]
    resultado = []
    print('Insira o valor da primeira entrada: ')
    m1 = input()
    if isinstance(m1,str)==True:
        m1 = np.random.randn()
    print('Insira o valor da segunda entrada: ')
    m2 = input()
    if isinstance(m2,str)==True:
        m2 = np.random.randn()
    print('Insira o valor do primeiro peso: ')
    w1 = input()
    if isinstance(w1,str)==True:
        w1 = np.random.randn()
    print('Insira o valor do segundo peso: ')
    w2 = input()
    if isinstance(w2,str)==True:
        w2 = np.random.randn()
    print('Insira o valor do terceiro peso: ')
    w3 = input()
    if isinstance(w3,str)==True:
        w3 = np.random.randn()
    print('Insira o valor do quarto peso: ')
    w4 = input()
    if isinstance(w4,str)==True:
        w4 = np.random.randn()
    print('Insira o valor do quinto peso: ')
    w5 = input()
    if isinstance(w5,str)==True:
        w5 = np.random.randn()
    print('Insira o valor do sexto peso: ')
    w6 = input()
    if isinstance(w6,str)==True:
        w6 = np.random.randn()
    
    meio = [m1*(w1 + w3),m2*(w2*w4)]
    for i in range(0,2):
        neuronio.append(sigmoid(meio[i]))
    fim = sigmoid(neuronio[0])*w5 + sigmoid(neuronio[1])*w6
    resultado = np.append(neuronio,fim)
    print('Os neurônios intermediários valem ',resultado[0],' e ',resultado[1],' , respectivamente. Já o axônio vale ',resultado[2])
    return resultado

