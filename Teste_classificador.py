import os
import csv
import skfuzzy as skf
import scipy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import fftpack

numfiles = 53

FS = 1000
T = 1/FS
aceleracao = {}


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
        N = len(arquivo)
        t = np.arange(0,0.001*len(aceleracao[l,k]),T)
        velocidade = T*aceleracao[l,k]
        deslocamento = T*velocidade
        sample_freq = fftpack.fftfreq(len(deslocamento),d=T)
        deslocamento_fft = fftpack.fft(deslocamento)
        pidxs = np.where(sample_freq > 0)
        freqs = sample_freq[pidxs]
        PSD = np.abs(deslocamento_fft)[pidxs]
        

        #plt.figure(1)
        #plt.title("Sinal original")
        #plt.plot(t,deslocamento)

        #plt.figure(2)
        #plt.title("Sinal da transformada")
        #plt.plot(freq[f],PSD[:,1][f])
        #plt.show()
       
        
        
