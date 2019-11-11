import csv
import skfuzzy as skf
import scipy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.fftpack as spfft
import scipy.signal
from scipy import fftpack

numfiles = 53

FS = 1000 #frequência de aquisição, 1000 Hz
T = 1/FS
# número de amostrar por segundo, 1000/s
aceleracao = {}
velocidade = {}
deslocamento = {}
deslocamento_fft = {}
PSD = {}
PSD_3d = {}
freq = {}
fftfreq = {}
signalAmplitude = {}
Fm=1000
potencia_pico = {}
frequencia_pico = {}
t = {}
PSDabs = {}
F = {}
D = {}
f={}
PSP = {}

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
        t[l,k] = np.linspace(0,(len(arquivo)+1)/FS,len(arquivo),endpoint=False)
        aceleracao[l,k] = 1000*arquivo[:,0:3]
        velocidade[l,k] = T*aceleracao[l,k]
        deslocamento[l,k] = T*velocidade[l,k]
        #D[l,k] = abs(fftpack.fft(deslocamento[l,k]))
        #F[l,k] = np.fft.fftfreq(len(D[l,k]),d=T)
        #ind = np.arange(0,len(D[l,k])/2+1)
        #ind = ind.astype(int)
        #PSD[l,k] = np.abs(D[l,k][ind]) - np.abs(D[l,k][-ind])**2
        #PSDabs[l,k] = PSD[l,k].sum(axis=1) 
        #plt.plot(F[l,k][ind],PSDabs[l,k])
        #plt.show()
        #plt.plot(F[l,k],D[l,k])
        #plt.show()
        f[l,k], PSD[l,k] = scipy.signal.periodogram(deslocamento[l,k],nfft=None)
        #freq[l,k], PSP[l,k] = scipy.signal.welch(deslocamento[l,k],FS)

        
        

        #PSD_3d[l,k] = np.abs(deslocamento_fft[l,k])
        #PSD[l,k] = PSD_3d[l,k].sum(axis = 1)
        #
        #signalAmplitude[l,k] = deslocamento[l,k].sum(axis = 1)
        # plot the signal in frequency domain
        # display the plots
        #plt.show()
        #deslocamento_fft[l,k] = fftpack.fft(deslocamento[l,k])
        #PSD_3d[l,k] = np.abs(deslocamento_fft[l,k])**2
        #PSD[l,k] = PSD_3d[l,k].sum(axis = 1)
        #fftfreq[l,k] = fftpack.fftfreq(len(deslocamento[l,k]), d = T)
        #i = fftfreq [l,k] > 0
        #freq = fftfreq[l,k][i]
        #PSDP = PSD[l,k][i]
        #plt.plot(t[l,k],deslocamento[l,k])
        #plt.plot(fftfreq[l,k][i],PSD[l,k][i])
        #plt.show()
        #PSD_3d[l,k] = abs(deslocamento_fft[l,k])
        #PSD[l,k] = PSD_3d[l,k].sum(axis = 1)
        #potencia_pico[l,k] = np.amax(PSD[l,k][i])
        #indice_pico = np.where(PSD[l,k][i]==np.amax(PSD[l,k][i]))
        #frequencia_pico[l,k] = fftfreq[l,k][i][indice_pico]                             
        #print(potencia_pico[l,k],frequencia_pico[l,k])
        #plt.magnitude_spectrum(deslocamento[l,k][:,0],Fs=1000)
        #plt.magnitude_spectrum(deslocamento[l,k][:,1],Fs=1000)
        #plt.magnitude_spectrum(deslocamento[l,k][:,2],Fs=1000)
        #plt.show()



       
     
#for l in range(0,6):
   #for k in range(1,11):
     #   plt.figure(1)
    #    plt.title('Sinal da transformada do voluntario %i' %k)
   #     plt.plot(f[l,k],2/FS*PSD_3d[l,k][:FS//2])
  #      v = [0,500,0,1]
 #       plt.axis(v)
        #print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
#plt.show()
    #for k in range(11,21):
     #   plt.figure(1)
      #  plt.title('Sinal da transformada do voluntario %i' %k)
       # plt.plot(freq[l,k],PSD[l,k])
        #v = [0,500,0,5]
        #plt.axis(v)
        #print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
    #plt.show()
    #for k in range(21,31):
     #   plt.figure(1)
      #  plt.title('Sinal da transformada do voluntario %i' %k)
       # plt.plot(freq[l,k],PSD[l,k])
        #v = [0,500,0,5]
        #plt.axis(v)
        #print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
    #plt.show()
    #for k in range(31,41):
     #   plt.figure(1)
      #  plt.title('Sinal da transformada do voluntario %i' %k)
       # plt.plot(freq[l,k],PSD[l,k])
        #v = [0,500,0,5]
       # plt.axis(v)
       # print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
    #plt.show()
   # for k in range(41,54):
    #    plt.figure(1)
     #   plt.title('Sinal da transformada do voluntario %i' %k)
      #  plt.plot(freq[l,k],PSD[l,k])
       # v = [0,500,0,5]
        #plt.axis(v)
        #print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[
