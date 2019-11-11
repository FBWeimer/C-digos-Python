import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.signal as signal
import skfuzzy as fuzzy
from skfuzzy import control
import statistics as st

numfiles = 53
FS = 1000
T = 1/1000
aceleracao, velocidade, deslocamento, PSD, PSDx, PSDy, PSDz, fx, fy, fz, f, potencia_pico, frequencia_pico = {},{},{},{},{},{},{},{},{},{},{},{},{}
v = [0.001,25,0,1000]

aux_arquivo = 'C:/Users/weime/OneDrive/Documentos/Estudo/I.A/Base de Dados/T0%k/%l/kinect_accelerometer.tsv'
movimento = ['Rest','Hands_in_pronation','Thumbs_up','Top_nose_left','Top_nose_right','Top_top']
Movimento = ['Repouso','Mãos em pronação','Polegares para cima','Dedo indicador esquerdo no nariz','Dedo indicador direito no nariz','Braço flexionado para frente']

for l in range(0,6):

        for k in range(1,numfiles+1):

            voluntario = str(k)
            define_movimento = aux_arquivo.replace('%l',movimento[l])
            define_voluntario = define_movimento.replace('%k',voluntario)
            local_arquivo = define_voluntario

            arquivo = pd.read_csv(local_arquivo, parse_dates=True, delim_whitespace=True, header=0)
            arquivo = arquivo.values

            aceleracao[l,k] = arquivo[:,0:3]

            aceleracaox = aceleracao[l,k][:,0]
            aceleracaoy = aceleracao[l,k][:,1]
            aceleracaoz = aceleracao[l,k][:,2]

            aceleracaototal = (aceleracaox**2+aceleracaoy**2+aceleracaoz**2)**(1/2)


            #fx[l,k], PSDx[l,k] = signal.welch(aceleracaox,FS,nperseg = len(aceleracaox))
            #fy[l,k], PSDy[l,k] = signal.welch(aceleracaoy,FS,nperseg = len(aceleracaoy))
            #fz[l,k], PSDz[l,k] = signal.welch(aceleracaoz,FS,nperseg = len(aceleracaoz))
            
            fx[l,k], PSDx[l,k] = signal.welch(aceleracaototal,FS,nperseg = len(aceleracaototal))
            indice1 = next(x for x, val in enumerate(fx[l,k]) if val > 2)
            indice2 = next(x for x, val in enumerate(fx[l,k]) if val > 25)
            f[l,k] = fx[l,k][indice1:indice2]
            PSD[l,k] = PSDx[l,k][indice1:indice2] #+ PSDy[l,k][indice1:]+ PSDz[l,k][indice1:]
            
            #velocidade[l,k] = T*aceleracao[l,k]
            #deslocamento[l,k] = T*velocidade[l,k]
            #deslocamentosx = deslocamento[l,k][:,0]
            #deslocamentosy = deslocamento[l,k][:,1]
            #deslocamentosz = deslocamento[l,k][:,2]

            #fx[l,k], PSDx[l,k] = signal.welch(deslocamentosx,FS,nperseg = len(deslocamentosx))
            #fy[l,k], PSDy[l,k] = signal.welch(deslocamentosy,FS,nperseg = len(deslocamentosy))
            #fz[l,k], PSDz[l,k] = signal.welch(deslocamentosz,FS,nperseg = len(deslocamentosz))
            #indice1 = next(x for x, val in enumerate(fx[l,k]) if val > 2)
            #f[l,k] = fx[l,k][indice1:]
            #PSD[l,k] = PSDx[l,k][indice1:] + PSDy[l,k][indice1:]+ PSDz[l,k][indice1:]

            potencia_pico[l,k] = np.amax(PSD[l,k])
            indice = np.where(PSD[l,k]==potencia_pico[l,k])
            frequencia_pico[l,k] = f[l,k][indice]
       

for l in range(0,6):

        for k in range(1,11):
            plt.title('Movimento %s' %Movimento[l])
            plt.plot(f[l,k],PSD[l,k],label = 'Voluntário %s' %k)
            plt.axis(v)
            plt.legend()
            print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
        plt.show()

        for k in range(11,21):
            plt.title('Movimento %s' %Movimento[l])
            plt.plot(f[l,k],PSD[l,k],label = 'Voluntário %s' %k)
            plt.axis(v)
            plt.legend()
            print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
        plt.show()
        for k in range(21,31):
            plt.title('Movimento %s' %Movimento[l])
            plt.plot(f[l,k],PSD[l,k],label = 'Voluntário %s' %k)
            plt.axis(v)
            plt.legend()
            print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
        plt.show()
        for k in range(31,41):
            plt.title('Movimento %s' %Movimento[l])
            plt.plot(f[l,k],PSD[l,k],label = 'Voluntário %s' %k)
            plt.axis(v)
            plt.legend()
            print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
        plt.show()
        for k in range(41,54):
            plt.title('Movimento %s' %Movimento[l])
            plt.plot(f[l,k],PSD[l,k],label = 'Voluntário %s' %k)
            plt.axis(v)
            plt.legend()
            print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
        plt.show()
