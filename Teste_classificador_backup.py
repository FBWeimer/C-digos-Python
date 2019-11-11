import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.signal as signal

numfiles = 53
FS = 1000
T = 1/1000
aceleracao, velocidade, deslocamento, PSD, PSDx, PSDy, PSDz, fx, fy, fz, f, potencia_pico, frequencia_pico = {}, velocidade = {}
v = [0.001,25,0,0.05]

aux_arquivo = 'C:/Users/weime/OneDrive/Documentos/Estudo/I.A/Base de Dados/T0%k/%l/kinect_accelerometer.tsv'
movimento = ['Rest','Hands_in_pronation','Thumbs_up','Top_nose_left','Top_nose_right','Top_top']

for l in range(0,6):

        for k in range(1,numfiles+1):

            voluntario = str(k)
            define_movimento = aux_arquivo.replace('%l',movimento[l])
            define_voluntario = define_movimento.replace('%k',voluntario)
            local_arquivo = define_voluntario

            arquivo = pd.read_csv(local_arquivo, parse_dates=True, delim_whitespace=True, header=0)
            arquivo = arquivo.values

            aceleracao[l,k] = 1000*arquivo[:,0:3]
            velocidade[l,k] = T*aceleracao[l,k]
            deslocamento[l,k] = T*velocidade[l,k]
            deslocamentosx = deslocamento[l,k][:,0]
            deslocamentosy = deslocamento[l,k][:,1]
            deslocamentosz = deslocamento[l,k][:,2]

            fx[l,k], PSDx[l,k] = signal.welch(deslocamentosx,FS,nperseg = len(deslocamentosx))
            fy[l,k], PSDy[l,k] = signal.welch(deslocamentosy,FS,nperseg = len(deslocamentosy))
            fz[l,k], PSDz[l,k] = signal.welch(deslocamentosz,FS,nperseg = len(deslocamentosz))
            f[l,k] = fx[l,k][1,:]
            PSD[l,k] = PSDx[l,k] [1,:]+ PSDy[l,k] [1,:]+ PSDz[l,k][1,:]

            potencia_pico[l,k] = np.amax(PSD[l,k])
            indice = np.where(PSD[l,k]==potencia_pico[l,k])
            frequencia_pico[l,k] = f[indice]

            plt.plot(f[l,k],PSD[l,k])
            v = [0.001,25,0,0.05]
            plt.axis(v)
            plt.show()

for l in range(0,6):

        for k in range(21,31):
            #plt.title('Sinal da transformada do voluntario %i' %k)
            plt.plot(f[l,k],PSD[l,k])
            plt.axis(v)
            print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
        plt.show()

        for k in range(11,21):
        #plt.title('Sinal da transformada do voluntario %i' %k)
            plt.plot(f[l,k],PSD[l,k])
            plt.axis(v)
            print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
        #if k == 20:
        plt.show()
        for k in range(21,31):
            #plt.title('Sinal da transformada do voluntario %i' %k)
            plt.plot(f[l,k],PSD[l,k])
            plt.axis(v)
            print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
        plt.show()
        for k in range(31,41):
            #plt.title('Sinal da transformada do voluntario %i' %k)
            plt.plot(f[l,k],PSD[l,k])
            plt.axis(v)
            print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
        plt.show()
        for k in range(41,54):
            #plt.title('Sinal da transformada do voluntario %i' %k)
            plt.plot(f[l,k],PSD[l,k])
            plt.axis(v)
            print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
        plt.show()