import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def NN():
    
    m1 = 0.6
    m2 = 0.1
    w1 = 0.6
    w2 = 0.5
    w3 = 0.1
    w4 = 0.3
    w5 = 0.4
    w6 = 0.2
    
    neuronio=[]
    resultado = []
    meio = [m1*(w1 + w3),m2*(w2*w4)]
    for i in range(0,2):
        neuronio.append(sigmoid(meio[i]))
    fim = sigmoid(neuronio[0])*w5 + sigmoid(neuronio[1])*w6
    resultado = np.append(neuronio,fim)
    print('Os neurônios intermediários valem ',resultado[0],' e ',resultado[1],' , respectivamente. Já o axônio vale ',resultado[2])
    return resultado

