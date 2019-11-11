import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def NN(m1,m2,w1,w2,w3,w4,w5,w6):
    neuronio=[]
    resultado = []
    meio = [m1*(w1 + w3),m2*(w2*w4)]
    for i in range(0,2):
        neuronio.append(sigmoid(meio[i]))
    fim = sigmoid(neuronio[0])*w5 + sigmoid(neuronio[1])*w6
    resultado = np.append(neuronio,fim)
    print('Os neurônios intermediários valem ',resultado[0],' e ',resultado[1],' , respectivamente. Já o axônio vale ',resultado[2])
    return resultado

