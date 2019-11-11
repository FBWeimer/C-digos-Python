import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.signal as signal
import skfuzzy as fuzzy

numfiles = 53
FS = 1000
T = 1/1000
aceleracao, velocidade, deslocamento, PSD, PSDx, PSDy, PSDz, fx, fy, fz, f, potencia_pico, frequencia_pico, deslocamento_total, t = {},{},{},{},{},{},{},{},{},{},{},{},{},{},{}

frequencia_baixa, frequencia_media, frequencia_alta, potencia_baixa, potencia_media, potencia_alta = {},{},{},{},{},{}
frequencia_nivel_baixo, frequencia_nivel_medio, frequencia_nivel_alto, potencia_nivel_baixo, potencia_nivel_medio, potencia_nivel_alto = {},{},{},{},{},{}

v = [0.001,25,0,50]

aux_arquivo = 'C:/Users/weime/Documents/Base de Dados/T0%k/%l/kinect_accelerometer.tsv'
movimento = ['Rest','Hands_in_pronation','Thumbs_up','Top_nose_left','Top_nose_right','Top_top']
Movimento = ['Repouso','Mãos em pronação','Polegares para cima','Dedo indicador esquerdo no nariz','Dedo indicador direito no nariz','Braço flexionado para frente']


porcentagem = np.arange(0.,101.,1.)

parkinson_baixo = fuzzy.trimf(porcentagem,[0,0,30])
parkinson_medio = fuzzy.trimf(porcentagem,[25,50,85])
parkinson_alto = fuzzy.trimf(porcentagem,[75,100,100])

essencial_baixo = fuzzy.trimf(porcentagem,[0.,0.,30.])
essencial_medio = fuzzy.trimf(porcentagem,[25.,50.,85.])
essencial_alto = fuzzy.trimf(porcentagem,[75.,100.,100.])

distonico_baixo = fuzzy.trimf(porcentagem,[0,0,30])
distonico_medio = fuzzy.trimf(porcentagem,[25,50,85])
distonico_alto = fuzzy.trimf(porcentagem,[75,100,100])

funcional_baixo = fuzzy.trimf(porcentagem,[0,0,30])
funcional_medio = fuzzy.trimf(porcentagem,[25,50,85])
funcional_alto = fuzzy.trimf(porcentagem,[75,100,100])

saudavel_baixo = fuzzy.trimf(porcentagem,[0,0,30])
saudavel_medio = fuzzy.trimf(porcentagem,[25,50,85])
saudavel_alto = fuzzy.trimf(porcentagem,[75,100,100])

p = [0,100,0,1]
plt.plot(saudavel_baixo,label = 'Probabilidade Baixa')
plt.plot(saudavel_medio,label = 'Probabilidade Média')
plt.plot(saudavel_alto,label = 'Probabilidade Alta')
plt.axis(p)
plt.xlabel('Probabilidade (%)')
plt.ylabel('Grau de Pertencimento')
plt.title()
plt.show()


resultado_parkinson = np.zeros([6,numfiles+1],dtype=float)
resultado_essencial = np.zeros([6,numfiles+1],dtype=float)
resultado_distonico = np.zeros([6,numfiles+1],dtype=float)
resultado_funcional = np.zeros([6,numfiles+1],dtype=float)
resultado_saudavel = np.zeros([6,numfiles+1],dtype=float)


for l in range(0,6):

        for k in range(1,numfiles+1):

            voluntario = str(k)
            define_movimento = aux_arquivo.replace('%l',movimento[l])
            define_voluntario = define_movimento.replace('%k',voluntario)
            local_arquivo = define_voluntario

            arquivo = pd.read_csv(local_arquivo, parse_dates=True, delim_whitespace=True, header=0)
            arquivo = arquivo.values

            aceleracao[l,k] = arquivo[:,0:3]
            velocidade[l,k] = aceleracao[l,k]
            deslocamento[l,k] = T*velocidade[l,k]
            deslocamentosx = deslocamento[l,k][:,0]
            deslocamentosy = deslocamento[l,k][:,1]
            deslocamentosz = deslocamento[l,k][:,2]
            aceleracaox = aceleracao[l,k][:,0]
            aceleracaoy = aceleracao[l,k][:,1]
            aceleracaoz = aceleracao[l,k][:,2]

            deslocamento_total[l,k] = ((deslocamentosx)**2 + (deslocamentosy)**2 + (deslocamentosz)**2)**(1/2)
            t[l,k] = np.arange(0,len(deslocamento_total[l,k])/1000,T)

            aceleracaototal = (aceleracaox**2+aceleracaoy**2+aceleracaoz**2)**(1/2)

            #fx[l,k], PSDx[l,k] = signal.welch(aceleracaox,FS,nperseg = len(aceleracaox))
            #fy[l,k], PSDy[l,k] = signal.welch(aceleracaoy,FS,nperseg = len(aceleracaoy))
            #fz[l,k], PSDz[l,k] = signal.welch(aceleracaoz,FS,nperseg = len(aceleracaoz))
            
            fx[l,k], PSDx[l,k] = signal.welch(aceleracaototal,FS,nperseg = len(aceleracaototal))
            indice1 = next(x for x, val in enumerate(fx[l,k]) if val > 2)
            indice2 = next(x for x, val in enumerate(fx[l,k]) if val > 25)
            f[l,k] = fx[l,k][indice1:indice2]
            PSD[l,k] = PSDx[l,k][indice1:indice2] #+ PSDy[l,k][indice1:]+ PSDz[l,k][indice1:]

            potencia_pico[l,k] = np.amax(PSD[l,k])
            indice = np.where(PSD[l,k]==potencia_pico[l,k])
            frequencia_pico[l,k] = f[l,k][indice]


            frequencia_baixa[l,k] = fuzzy.trimf(f[l,k],[2,3,4])
            frequencia_media[l,k] = fuzzy.trimf(f[l,k],[3,5,7])
            frequencia_alta[l,k] = fuzzy.trapmf(f[l,k],[6,8,25,25])

            a = [2,25,0,1]
            plt.plot(frequencia_baixa[l,k],label = 'Frequência Baixa')
            plt.plot(frequencia_media[l,k],label = 'Frequência Média')
            plt.plot(frequencia_alta[l,k], label = 'Frequência Alta')
            plt.axis(a)
            plt.xlabel('Frequência (Hz)')
            plt.ylabel('Grau de Pertencimento')
            plt.show()
            
            
            potencia_baixa[l,k] = fuzzy.trimf(PSD[l,k],[0,10,20])
            potencia_media[l,k] = fuzzy.trimf(PSD[l,k],[15,50,90])
            potencia_alta[l,k] = fuzzy.trapmf(PSD[l,k],[80,100,10000,10000])

            b = [0,10000,0,1]
            plt.plot(potencia_baixa[l,k],label = 'Energia Baixa')
            plt.plot(potencia_media[l,k],label = 'Energia Média')
            plt.plot(potencia_alta[l,k], label = 'Energia Alta')
            plt.axis(b)
            plt.xlabel('Energia (m²/s²)')
            plt.ylabel('Grau de Pertencimento')
            plt.show()

            frequencia_nivel_baixo[l,k] = fuzzy.interp_membership(f[l,k], frequencia_baixa[l,k], frequencia_pico[l,k])
            frequencia_nivel_medio[l,k] = fuzzy.interp_membership(f[l,k], frequencia_media[l,k], frequencia_pico[l,k])
            frequencia_nivel_alto[l,k] = fuzzy.interp_membership(f[l,k], frequencia_alta[l,k], frequencia_pico[l,k])

            potencia_nivel_baixo[l,k] = np.amax(potencia_baixa[l,k])
            potencia_nivel_medio[l,k] = np.amax(potencia_media[l,k])
            potencia_nivel_alto[l,k] = np.amax(potencia_alta[l,k])


#z = [0,45,0,1.5]
#plt.title('Deslocamentos para a posição de repouso')
#plt.plot(t[0,1],deslocamento_total[0,1],label = 'Saudável')
#plt.plot(t[0,8],deslocamento_total[0,8],'-',label = 'Essencial')
#plt.plot(t[0,53],deslocamento_total[0,53],'--',label = 'Funcional')
#plt.plot(t[0,41],deslocamento_total[0,41],'-.',label = 'Distônico')
#plt.plot(t[0,12],deslocamento_total[0,12],':',label = 'Parkinson')
#plt.axis(z)
#plt.legend()
#plt.xlabel ('Tempo (s)')
#plt.ylabel ('Deslocamento (mm)')
#plt.show()


#m = [0,25,0,5000]
#plt.title('Densidade espectral de energia para a posição de repouso')
#plt.plot(f[0,1],PSD[0,1],label = 'Saudável')
#plt.plot(f[0,5],PSD[0,5],label = 'Essencial')
#plt.plot(f[0,53],PSD[0,53],label = 'Funcional')
#plt.plot(f[0,41],PSD[0,41],label = 'Distônico')
#plt.plot(f[0,12],PSD[0,12],label = 'Parkinson')
#plt.plot(f[0,9],PSD[0,9],label = 'Outro')
#plt.axis(m)
#plt.legend()
#plt.xlabel ('Frequência (Hz)')
#plt.ylabel ('PSD (m²/s²)')
#plt.show()
            
            
##Movimento 1
for l in range(0,6):
        for k in range(1,numfiles+1):
                if l==0:

                        parkinson_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[0,k],potencia_nivel_baixo[0,k]),parkinson_baixo)
                        parkinson_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[0,k],potencia_nivel_medio[0,k]),parkinson_medio)
                        parkinson_mp1 = np.fmin(np.fmin(frequencia_nivel_baixo[0,k],potencia_nivel_alto[0,k]),parkinson_alto)
                        parkinson_pp2 = np.fmin(np.fmin(frequencia_nivel_medio[0,k],potencia_nivel_baixo[0,k]),parkinson_baixo)
                        parkinson_pm2 = np.fmin(np.fmin(frequencia_nivel_medio[0,k],potencia_nivel_medio[0,k]),parkinson_medio)
                        parkinson_mp2 = np.fmin(np.fmin(frequencia_nivel_medio[0,k],potencia_nivel_alto[0,k]),parkinson_alto)
                        parkinson_pp3 = np.fmin(np.fmin(frequencia_nivel_alto[0,k],potencia_nivel_baixo[0,k]),parkinson_baixo)
                        parkinson_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[0,k],potencia_nivel_medio[0,k]),parkinson_baixo)
                        parkinson_pp5 = np.fmin(np.fmin(frequencia_nivel_alto[0,k],potencia_nivel_alto[0,k]),parkinson_baixo)
                        

                        essencial_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[0,k],potencia_nivel_baixo[0,k]),essencial_baixo)
                        essencial_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[0,k],potencia_nivel_medio[0,k]),essencial_baixo)
                        essencial_pp3 = np.fmin(np.fmin(frequencia_nivel_baixo[0,k],potencia_nivel_alto[0,k]),essencial_baixo)
                        essencial_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[0,k],potencia_nivel_baixo[0,k]),essencial_alto)
                        essencial_pm1 = np.fmin(np.fmin(frequencia_nivel_medio[0,k],potencia_nivel_medio[0,k]),essencial_medio)
                        essencial_pp4 = np.fmin(np.fmin(frequencia_nivel_medio[0,k],potencia_nivel_alto[0,k]),essencial_baixo)
                        essencial_pm2 = np.fmin(np.fmin(frequencia_nivel_alto[0,k],potencia_nivel_baixo[0,k]),essencial_medio)
                        essencial_pp5 = np.fmin(np.fmin(frequencia_nivel_alto[0,k],potencia_nivel_medio[0,k]),essencial_baixo)
                        essencial_pp6 = np.fmin(np.fmin(frequencia_nivel_alto[0,k],potencia_nivel_alto[0,k]),essencial_baixo)
                        

                        distonico_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[0,k],potencia_nivel_baixo[0,k]),distonico_medio)
                        distonico_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[0,k],potencia_nivel_medio[0,k]),distonico_baixo)
                        distonico_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[0,k],potencia_nivel_alto[0,k]),distonico_baixo)
                        distonico_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[0,k],potencia_nivel_baixo[0,k]),distonico_alto)
                        distonico_pm2 = np.fmin(np.fmin(frequencia_nivel_medio[0,k],potencia_nivel_medio[0,k]),distonico_medio)
                        distonico_pm3 = np.fmin(np.fmin(frequencia_nivel_medio[0,k],potencia_nivel_alto[0,k]),distonico_medio)
                        distonico_mp2 = np.fmin(np.fmin(frequencia_nivel_alto[0,k],potencia_nivel_baixo[0,k]),distonico_alto)
                        distonico_pp3 = np.fmin(np.fmin(frequencia_nivel_alto[0,k],potencia_nivel_medio[0,k]),distonico_baixo)
                        distonico_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[0,k],potencia_nivel_alto[0,k]),distonico_baixo)
                        

                        funcional_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[0,k],potencia_nivel_baixo[0,k]),funcional_medio)
                        funcional_pm2 = np.fmin(np.fmin(frequencia_nivel_baixo[0,k],potencia_nivel_medio[0,k]),funcional_medio)
                        funcional_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[0,k],potencia_nivel_alto[0,k]),funcional_baixo)
                        funcional_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[0,k],potencia_nivel_baixo[0,k]),funcional_alto)
                        funcional_mp2 = np.fmin(np.fmin(frequencia_nivel_medio[0,k],potencia_nivel_medio[0,k]),funcional_alto)
                        funcional_pp2 = np.fmin(np.fmin(frequencia_nivel_medio[0,k],potencia_nivel_alto[0,k]),funcional_baixo)
                        funcional_pp3 = np.fmin(np.fmin(frequencia_nivel_alto[0,k],potencia_nivel_baixo[0,k]),funcional_baixo)
                        funcional_mp3 = np.fmin(np.fmin(frequencia_nivel_alto[0,k],potencia_nivel_medio[0,k]),funcional_alto)
                        funcional_mp4 = np.fmin(np.fmin(frequencia_nivel_alto[0,k],potencia_nivel_alto[0,k]),funcional_alto)
                        

                        saudavel_mp1 = np.fmin(np.fmin(frequencia_nivel_baixo[0,k],potencia_nivel_baixo[0,k]),saudavel_alto)
                        saudavel_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[0,k],potencia_nivel_medio[0,k]),saudavel_baixo)
                        saudavel_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[0,k],potencia_nivel_alto[0,k]),saudavel_baixo)
                        saudavel_mp2 = np.fmin(np.fmin(frequencia_nivel_medio[0,k],potencia_nivel_baixo[0,k]), saudavel_alto)
                        saudavel_pp3 = np.fmin(np.fmin(frequencia_nivel_medio[0,k],potencia_nivel_medio[0,k]),saudavel_baixo)
                        saudavel_pp4 = np.fmin(np.fmin(frequencia_nivel_medio[0,k],potencia_nivel_alto[0,k]),saudavel_baixo)
                        saudavel_mp3 = np.fmin(np.fmin(frequencia_nivel_alto[0,k],potencia_nivel_baixo[0,k]),saudavel_alto)
                        saudavel_pp5 = np.fmin(np.fmin(frequencia_nivel_alto[0,k],potencia_nivel_medio[0,k]),saudavel_baixo)
                        saudavel_pp6 = np.fmin(np.fmin(frequencia_nivel_alto[0,k],potencia_nivel_alto[0,k]),saudavel_baixo)


                        agregador_parkinson = np.fmax(np.fmax(np.fmax(np.fmax(parkinson_pp1,parkinson_pm1),np.fmax(parkinson_mp1, parkinson_pp2)),np.fmax(np.fmax(parkinson_pm2,parkinson_mp2),np.fmax(parkinson_pp3,parkinson_pp4))),parkinson_pp5)
                        agregador_essencial = np.fmax(np.fmax(np.fmax(np.fmax(essencial_pp1,parkinson_pp2),np.fmax(essencial_pp3, essencial_mp1)),np.fmax(np.fmax(essencial_pm1,essencial_pp4),np.fmax(essencial_pm2,essencial_pp5))),essencial_pp6)
                        agregador_distonico = np.fmax(np.fmax(np.fmax(np.fmax(distonico_pm1,distonico_pp1),np.fmax(distonico_pp2, distonico_mp1)),np.fmax(np.fmax(distonico_pm2,distonico_pm3),np.fmax(distonico_mp2,distonico_pp3))),distonico_pp4)
                        agregador_funcional = np.fmax(np.fmax(np.fmax(np.fmax(funcional_pm1,funcional_pm2),np.fmax(funcional_pp1, funcional_mp1)),np.fmax(np.fmax(funcional_mp2,funcional_pp2),np.fmax(funcional_pp3,funcional_mp3))),funcional_mp4)
                        agregador_saudavel = np.fmax(np.fmax(np.fmax(np.fmax(saudavel_mp1,saudavel_pp1),np.fmax(saudavel_pp2, saudavel_mp2)),np.fmax(np.fmax(saudavel_pp3,saudavel_pp4),np.fmax(saudavel_mp3,saudavel_pp5))),saudavel_pp6)

                        
                        resultado_parkinson[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_parkinson,'centroid'))
                        resultado_essencial[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_essencial,'centroid'))
                        resultado_distonico[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_distonico,'centroid'))
                        resultado_funcional[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_funcional,'centroid'))
                        resultado_saudavel[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_saudavel,'centroid'))
        
#Movimento 2

for l in range(0,6):
        for k in range(1,numfiles+1):
                if l==1:
        

                        parkinson_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[1,k],potencia_nivel_baixo[1,k]),parkinson_medio)
                        parkinson_pm2 = np.fmin(np.fmin(frequencia_nivel_baixo[1,k],potencia_nivel_medio[1,k]),parkinson_medio)
                        parkinson_pm3 = np.fmin(np.fmin(frequencia_nivel_baixo[1,k],potencia_nivel_alto[1,k]),parkinson_medio)
                        parkinson_pm4 = np.fmin(np.fmin(frequencia_nivel_medio[1,k],potencia_nivel_baixo[1,k]),parkinson_medio)
                        parkinson_pm5 = np.fmin(np.fmin(frequencia_nivel_medio[1,k],potencia_nivel_medio[1,k]),parkinson_medio)
                        parkinson_pp1 = np.fmin(np.fmin(frequencia_nivel_medio[1,k],potencia_nivel_alto[1,k]),parkinson_baixo)
                        parkinson_pp2 = np.fmin(np.fmin(frequencia_nivel_alto[1,k],potencia_nivel_baixo[1,k]),parkinson_baixo)
                        parkinson_pp3 = np.fmin(np.fmin(frequencia_nivel_alto[1,k],potencia_nivel_medio[1,k]),parkinson_baixo)
                        parkinson_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[1,k],potencia_nivel_alto[1,k]),parkinson_baixo)
                        

                        essencial_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[1,k],potencia_nivel_baixo[1,k]),essencial_medio)
                        essencial_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[1,k],potencia_nivel_medio[1,k]),essencial_baixo)
                        essencial_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[1,k],potencia_nivel_alto[1,k]),essencial_baixo)
                        essencial_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[1,k],potencia_nivel_baixo[1,k]),essencial_alto)
                        essencial_mp2 = np.fmin(np.fmin(frequencia_nivel_medio[1,k],potencia_nivel_medio[1,k]),essencial_alto)
                        essencial_mp3 = np.fmin(np.fmin(frequencia_nivel_medio[1,k],potencia_nivel_alto[1,k]),essencial_alto)
                        essencial_mp4 = np.fmin(np.fmin(frequencia_nivel_alto[1,k],potencia_nivel_baixo[1,k]),essencial_alto)
                        essencial_pp3 = np.fmin(np.fmin(frequencia_nivel_alto[1,k],potencia_nivel_medio[1,k]),essencial_baixo)
                        essencial_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[1,k],potencia_nivel_alto[1,k]),essencial_baixo)
                        

                        distonico_mp1 = np.fmin(np.fmin(frequencia_nivel_baixo[1,k],potencia_nivel_baixo[1,k]),distonico_alto)
                        distonico_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[1,k],potencia_nivel_medio[1,k]),distonico_medio)
                        distonico_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[1,k],potencia_nivel_alto[1,k]),distonico_baixo)
                        distonico_mp2 = np.fmin(np.fmin(frequencia_nivel_medio[1,k],potencia_nivel_baixo[1,k]),distonico_alto)
                        distonico_mp3 = np.fmin(np.fmin(frequencia_nivel_medio[1,k],potencia_nivel_medio[1,k]),distonico_alto)
                        distonico_pp2 = np.fmin(np.fmin(frequencia_nivel_medio[1,k],potencia_nivel_alto[1,k]),distonico_baixo)
                        distonico_pp3 = np.fmin(np.fmin(frequencia_nivel_alto[1,k],potencia_nivel_baixo[1,k]),distonico_baixo)
                        distonico_mp4 = np.fmin(np.fmin(frequencia_nivel_alto[1,k],potencia_nivel_medio[1,k]),distonico_alto)
                        distonico_pm2 = np.fmin(np.fmin(frequencia_nivel_alto[1,k],potencia_nivel_alto[1,k]),distonico_medio)
                        

                        funcional_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[1,k],potencia_nivel_baixo[1,k]),funcional_baixo)
                        funcional_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[1,k],potencia_nivel_medio[1,k]),funcional_baixo)
                        funcional_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[1,k],potencia_nivel_alto[1,k]),funcional_medio)
                        funcional_pp3 = np.fmin(np.fmin(frequencia_nivel_medio[1,k],potencia_nivel_baixo[1,k]),funcional_baixo)
                        funcional_pp4 = np.fmin(np.fmin(frequencia_nivel_medio[1,k],potencia_nivel_medio[1,k]),funcional_baixo)
                        funcional_mp2 = np.fmin(np.fmin(frequencia_nivel_medio[1,k],potencia_nivel_alto[1,k]),funcional_alto)
                        funcional_pp5 = np.fmin(np.fmin(frequencia_nivel_alto[1,k],potencia_nivel_baixo[1,k]),funcional_baixo)
                        funcional_pm2 = np.fmin(np.fmin(frequencia_nivel_alto[1,k],potencia_nivel_medio[1,k]),funcional_medio)
                        funcional_pm3 = np.fmin(np.fmin(frequencia_nivel_alto[1,k],potencia_nivel_alto[1,k]),funcional_medio)
                        

                        saudavel_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[1,k],potencia_nivel_baixo[1,k]),saudavel_baixo)
                        saudavel_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[1,k],potencia_nivel_medio[1,k]),saudavel_baixo)
                        saudavel_pp3 = np.fmin(np.fmin(frequencia_nivel_baixo[1,k],potencia_nivel_alto[1,k]),saudavel_baixo)
                        saudavel_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[1,k],potencia_nivel_baixo[1,k]),saudavel_alto)
                        saudavel_pp4 = np.fmin(np.fmin(frequencia_nivel_medio[1,k],potencia_nivel_medio[1,k]),saudavel_baixo)
                        saudavel_pp5 = np.fmin(np.fmin(frequencia_nivel_medio[1,k],potencia_nivel_alto[1,k]),saudavel_baixo)
                        saudavel_mp2 = np.fmin(np.fmin(frequencia_nivel_alto[1,k],potencia_nivel_baixo[1,k]),saudavel_alto)
                        saudavel_pp6 = np.fmin(np.fmin(frequencia_nivel_alto[1,k],potencia_nivel_medio[1,k]),saudavel_baixo)
                        saudavel_pp7 = np.fmin(np.fmin(frequencia_nivel_alto[1,k],potencia_nivel_alto[1,k]),saudavel_baixo)


                        agregador_parkinson = np.fmax(np.fmax(np.fmax(np.fmax(parkinson_pm1,parkinson_pm2),np.fmax(parkinson_pm3, parkinson_pm4)),np.fmax(np.fmax(parkinson_pm5,parkinson_pp1),np.fmax(parkinson_pp2,parkinson_pp3))),parkinson_pp4)
                        agregador_essencial = np.fmax(np.fmax(np.fmax(np.fmax(essencial_pm1,parkinson_pp1),np.fmax(essencial_pp2, essencial_mp1)),np.fmax(np.fmax(essencial_mp2,essencial_mp3),np.fmax(essencial_mp4,essencial_pp3))),essencial_pp4)
                        agregador_distonico = np.fmax(np.fmax(np.fmax(np.fmax(distonico_mp1,distonico_pm1),np.fmax(distonico_pp1, distonico_mp2)),np.fmax(np.fmax(distonico_mp3,distonico_pp2),np.fmax(distonico_pp3,distonico_mp4))),distonico_pm2)
                        agregador_funcional = np.fmax(np.fmax(np.fmax(np.fmax(funcional_pp1,funcional_pp2),np.fmax(funcional_pm1, funcional_pp3)),np.fmax(np.fmax(funcional_pp4,funcional_mp2),np.fmax(funcional_pp5,funcional_pm2))),funcional_pm3)
                        agregador_saudavel = np.fmax(np.fmax(np.fmax(np.fmax(saudavel_pp1,saudavel_pp2),np.fmax(saudavel_pp3, saudavel_mp1)),np.fmax(np.fmax(saudavel_pp4,saudavel_pp5),np.fmax(saudavel_mp2,saudavel_pp6))),saudavel_pp7)


                        resultado_parkinson[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_parkinson,'centroid'))
                        resultado_essencial[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_essencial,'centroid'))
                        resultado_distonico[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_distonico,'centroid'))
                        resultado_funcional[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_funcional,'centroid'))
                        resultado_saudavel[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_saudavel,'centroid'))
        
#Movimento 3


for l in range(0,6):
        for k in range(1,numfiles+1):
                if l==2:
                        parkinson_mp1 = np.fmin(np.fmin(frequencia_nivel_baixo[2,k],potencia_nivel_baixo[2,k]),parkinson_alto)
                        parkinson_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[2,k],potencia_nivel_medio[2,k]),parkinson_medio)
                        parkinson_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[2,k],potencia_nivel_alto[2,k]),parkinson_baixo)
                        parkinson_pm2 = np.fmin(np.fmin(frequencia_nivel_medio[2,k],potencia_nivel_baixo[2,k]),parkinson_medio)
                        parkinson_pm3 = np.fmin(np.fmin(frequencia_nivel_medio[2,k],potencia_nivel_medio[2,k]),parkinson_medio)
                        parkinson_pm4 = np.fmin(np.fmin(frequencia_nivel_medio[2,k],potencia_nivel_alto[2,k]),parkinson_medio)
                        parkinson_pp2 = np.fmin(np.fmin(frequencia_nivel_alto[2,k],potencia_nivel_baixo[2,k]),parkinson_baixo)
                        parkinson_pp3 = np.fmin(np.fmin(frequencia_nivel_alto[2,k],potencia_nivel_medio[2,k]),parkinson_baixo)
                        parkinson_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[2,k],potencia_nivel_alto[2,k]),parkinson_baixo)
                        

                        essencial_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[2,k],potencia_nivel_baixo[2,k]),essencial_baixo)
                        essencial_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[2,k],potencia_nivel_medio[2,k]),essencial_medio)
                        essencial_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[2,k],potencia_nivel_alto[2,k]),essencial_baixo)
                        essencial_pm2 = np.fmin(np.fmin(frequencia_nivel_medio[2,k],potencia_nivel_baixo[2,k]),essencial_medio)
                        essencial_pm3 = np.fmin(np.fmin(frequencia_nivel_medio[2,k],potencia_nivel_medio[2,k]),essencial_medio)
                        essencial_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[2,k],potencia_nivel_alto[2,k]),essencial_alto)
                        essencial_pp3 = np.fmin(np.fmin(frequencia_nivel_alto[2,k],potencia_nivel_baixo[2,k]),essencial_baixo)
                        essencial_pm4 = np.fmin(np.fmin(frequencia_nivel_alto[2,k],potencia_nivel_medio[2,k]),essencial_medio)
                        essencial_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[2,k],potencia_nivel_alto[2,k]),essencial_baixo)
                        

                        distonico_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[2,k],potencia_nivel_baixo[2,k]),distonico_baixo)
                        distonico_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[2,k],potencia_nivel_medio[2,k]),distonico_baixo)
                        distonico_pp3 = np.fmin(np.fmin(frequencia_nivel_baixo[2,k],potencia_nivel_alto[2,k]),distonico_baixo)
                        distonico_pp4 = np.fmin(np.fmin(frequencia_nivel_medio[2,k],potencia_nivel_baixo[2,k]),distonico_baixo)
                        distonico_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[2,k],potencia_nivel_medio[2,k]),distonico_alto)
                        distonico_mp2 = np.fmin(np.fmin(frequencia_nivel_medio[2,k],potencia_nivel_alto[2,k]),distonico_alto)
                        distonico_pp5 = np.fmin(np.fmin(frequencia_nivel_alto[2,k],potencia_nivel_baixo[2,k]),distonico_baixo)
                        distonico_pm1 = np.fmin(np.fmin(frequencia_nivel_alto[2,k],potencia_nivel_medio[2,k]),distonico_medio)
                        distonico_mp3 = np.fmin(np.fmin(frequencia_nivel_alto[2,k],potencia_nivel_alto[2,k]),distonico_alto)
                        

                        funcional_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[2,k],potencia_nivel_baixo[2,k]),funcional_baixo)
                        funcional_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[2,k],potencia_nivel_medio[2,k]),funcional_baixo)
                        funcional_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[2,k],potencia_nivel_alto[2,k]),funcional_medio)
                        funcional_pp3 = np.fmin(np.fmin(frequencia_nivel_medio[2,k],potencia_nivel_baixo[2,k]),funcional_baixo)
                        funcional_pp4 = np.fmin(np.fmin(frequencia_nivel_medio[2,k],potencia_nivel_medio[2,k]),funcional_baixo)
                        funcional_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[2,k],potencia_nivel_alto[2,k]),funcional_alto)
                        funcional_pm2 = np.fmin(np.fmin(frequencia_nivel_alto[2,k],potencia_nivel_baixo[2,k]),funcional_medio)
                        funcional_pm3 = np.fmin(np.fmin(frequencia_nivel_alto[2,k],potencia_nivel_medio[2,k]),funcional_medio)
                        funcional_mp2 = np.fmin(np.fmin(frequencia_nivel_alto[2,k],potencia_nivel_alto[2,k]),funcional_alto)
                        

                        saudavel_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[2,k],potencia_nivel_baixo[2,k]),saudavel_baixo)
                        saudavel_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[2,k],potencia_nivel_medio[2,k]),saudavel_baixo)
                        saudavel_mp1 = np.fmin(np.fmin(frequencia_nivel_baixo[2,k],potencia_nivel_alto[2,k]),saudavel_alto)
                        saudavel_mp2 = np.fmin(np.fmin(frequencia_nivel_medio[2,k],potencia_nivel_baixo[2,k]),saudavel_alto)
                        saudavel_pp3 = np.fmin(np.fmin(frequencia_nivel_medio[2,k],potencia_nivel_medio[2,k]),saudavel_baixo)
                        saudavel_mp3 = np.fmin(np.fmin(frequencia_nivel_medio[2,k],potencia_nivel_alto[2,k]),saudavel_alto)
                        saudavel_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[2,k],potencia_nivel_baixo[2,k]),saudavel_baixo)
                        saudavel_pp5 = np.fmin(np.fmin(frequencia_nivel_alto[2,k],potencia_nivel_medio[2,k]),saudavel_baixo)
                        saudavel_pp6 = np.fmin(np.fmin(frequencia_nivel_alto[2,k],potencia_nivel_alto[2,k]),saudavel_baixo)


                        agregador_parkinson = np.fmax(np.fmax(np.fmax(np.fmax(parkinson_mp1,parkinson_pm1),np.fmax(parkinson_pp1, parkinson_pm2)),np.fmax(np.fmax(parkinson_pm3,parkinson_pm4),np.fmax(parkinson_pp2,parkinson_pp3))),parkinson_pp4)
                        agregador_essencial = np.fmax(np.fmax(np.fmax(np.fmax(essencial_pp1,parkinson_pm1),np.fmax(essencial_pp2, essencial_pm2)),np.fmax(np.fmax(essencial_pm3,essencial_mp1),np.fmax(essencial_pp3,essencial_pm4))),essencial_pp4)
                        agregador_distonico = np.fmax(np.fmax(np.fmax(np.fmax(distonico_pp1,distonico_pp2),np.fmax(distonico_pp3, distonico_pp4)),np.fmax(np.fmax(distonico_mp1,distonico_mp2),np.fmax(distonico_pp5,distonico_pm1))),distonico_mp3)
                        agregador_funcional = np.fmax(np.fmax(np.fmax(np.fmax(funcional_pp1,funcional_pp2),np.fmax(funcional_pm1, funcional_pp3)),np.fmax(np.fmax(funcional_pp4,funcional_mp1),np.fmax(funcional_pm2,funcional_pm3))),funcional_mp2)
                        agregador_saudavel = np.fmax(np.fmax(np.fmax(np.fmax(saudavel_pp1,saudavel_pp2),np.fmax(saudavel_mp1, saudavel_mp2)),np.fmax(np.fmax(saudavel_pp3,saudavel_mp3),np.fmax(saudavel_pp4,saudavel_pp5))),saudavel_pp6)


                        resultado_parkinson[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_parkinson,'centroid'))
                        resultado_essencial[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_essencial,'centroid'))
                        resultado_distonico[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_distonico,'centroid'))
                        resultado_funcional[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_funcional,'centroid'))
                        resultado_saudavel[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_saudavel,'centroid'))
        
#Movimento 4


for l in range(0,6):
        for k in range(1,numfiles+1):
                if l==3:
                        parkinson_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[3,k],potencia_nivel_baixo[3,k]),parkinson_baixo)
                        parkinson_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[3,k],potencia_nivel_medio[3,k]),parkinson_baixo)
                        parkinson_pp3 = np.fmin(np.fmin(frequencia_nivel_baixo[3,k],potencia_nivel_alto[3,k]),parkinson_baixo)
                        parkinson_pm1 = np.fmin(np.fmin(frequencia_nivel_medio[3,k],potencia_nivel_baixo[3,k]),parkinson_medio)
                        parkinson_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[3,k],potencia_nivel_medio[3,k]),parkinson_alto)
                        parkinson_pm2 = np.fmin(np.fmin(frequencia_nivel_medio[3,k],potencia_nivel_alto[3,k]),parkinson_medio)
                        parkinson_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[3,k],potencia_nivel_baixo[3,k]),parkinson_baixo)
                        parkinson_pm3 = np.fmin(np.fmin(frequencia_nivel_alto[3,k],potencia_nivel_medio[3,k]),parkinson_medio)
                        parkinson_pp5 = np.fmin(np.fmin(frequencia_nivel_alto[3,k],potencia_nivel_alto[3,k]),parkinson_baixo)
                        

                        essencial_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[3,k],potencia_nivel_baixo[3,k]),essencial_medio)
                        essencial_pm2 = np.fmin(np.fmin(frequencia_nivel_baixo[3,k],potencia_nivel_medio[3,k]),essencial_medio)
                        essencial_pm3 = np.fmin(np.fmin(frequencia_nivel_baixo[3,k],potencia_nivel_alto[3,k]),essencial_medio)
                        essencial_pm4 = np.fmin(np.fmin(frequencia_nivel_medio[3,k],potencia_nivel_baixo[3,k]),essencial_medio)
                        essencial_pm5 = np.fmin(np.fmin(frequencia_nivel_medio[3,k],potencia_nivel_medio[3,k]),essencial_medio)
                        essencial_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[3,k],potencia_nivel_alto[3,k]),essencial_alto)
                        essencial_pp1 = np.fmin(np.fmin(frequencia_nivel_alto[3,k],potencia_nivel_baixo[3,k]),essencial_baixo)
                        essencial_pp2 = np.fmin(np.fmin(frequencia_nivel_alto[3,k],potencia_nivel_medio[3,k]),essencial_baixo)
                        essencial_pp3 = np.fmin(np.fmin(frequencia_nivel_alto[3,k],potencia_nivel_alto[3,k]),essencial_baixo)
                        

                        distonico_mp1 = np.fmin(np.fmin(frequencia_nivel_baixo[3,k],potencia_nivel_baixo[3,k]),distonico_alto)
                        distonico_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[3,k],potencia_nivel_medio[3,k]),distonico_medio)
                        distonico_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[3,k],potencia_nivel_alto[3,k]),distonico_baixo)
                        distonico_mp2 = np.fmin(np.fmin(frequencia_nivel_medio[3,k],potencia_nivel_baixo[3,k]),distonico_alto)
                        distonico_pp2 = np.fmin(np.fmin(frequencia_nivel_medio[3,k],potencia_nivel_medio[3,k]),distonico_baixo)
                        distonico_mp3 = np.fmin(np.fmin(frequencia_nivel_medio[3,k],potencia_nivel_alto[3,k]),distonico_alto)
                        distonico_pp3 = np.fmin(np.fmin(frequencia_nivel_alto[3,k],potencia_nivel_baixo[3,k]),distonico_baixo)
                        distonico_pm2 = np.fmin(np.fmin(frequencia_nivel_alto[3,k],potencia_nivel_medio[3,k]),distonico_medio)
                        distonico_pm3 = np.fmin(np.fmin(frequencia_nivel_alto[3,k],potencia_nivel_alto[3,k]),distonico_medio)

                        
                        funcional_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[3,k],potencia_nivel_baixo[3,k]),funcional_medio)
                        funcional_pm2 = np.fmin(np.fmin(frequencia_nivel_baixo[3,k],potencia_nivel_medio[3,k]),funcional_medio)
                        funcional_pm3 = np.fmin(np.fmin(frequencia_nivel_baixo[3,k],potencia_nivel_alto[3,k]),funcional_medio)
                        funcional_pp1 = np.fmin(np.fmin(frequencia_nivel_medio[3,k],potencia_nivel_baixo[3,k]),funcional_baixo)
                        funcional_pp2 = np.fmin(np.fmin(frequencia_nivel_medio[3,k],potencia_nivel_medio[3,k]),funcional_baixo)
                        funcional_pp3 = np.fmin(np.fmin(frequencia_nivel_medio[3,k],potencia_nivel_alto[3,k]),funcional_baixo)
                        funcional_pm4 = np.fmin(np.fmin(frequencia_nivel_alto[3,k],potencia_nivel_baixo[3,k]),funcional_medio)
                        funcional_mp4 = np.fmin(np.fmin(frequencia_nivel_alto[3,k],potencia_nivel_medio[3,k]),funcional_baixo)
                        funcional_mp5 = np.fmin(np.fmin(frequencia_nivel_alto[3,k],potencia_nivel_alto[3,k]),funcional_medio)
                        

                        saudavel_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[3,k],potencia_nivel_baixo[3,k]),saudavel_medio)
                        saudavel_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[3,k],potencia_nivel_medio[3,k]),saudavel_baixo)
                        saudavel_pm2 = np.fmin(np.fmin(frequencia_nivel_baixo[3,k],potencia_nivel_alto[3,k]),saudavel_medio)
                        saudavel_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[3,k],potencia_nivel_baixo[3,k]), saudavel_alto)
                        saudavel_pp2 = np.fmin(np.fmin(frequencia_nivel_medio[3,k],potencia_nivel_medio[3,k]),saudavel_baixo)
                        saudavel_pp3 = np.fmin(np.fmin(frequencia_nivel_medio[3,k],potencia_nivel_alto[3,k]),saudavel_baixo)
                        saudavel_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[3,k],potencia_nivel_baixo[3,k]),saudavel_baixo)
                        saudavel_pp5 = np.fmin(np.fmin(frequencia_nivel_alto[3,k],potencia_nivel_medio[3,k]),saudavel_baixo)
                        saudavel_pp6 = np.fmin(np.fmin(frequencia_nivel_alto[3,k],potencia_nivel_alto[3,k]),saudavel_baixo)


                        agregador_parkinson = np.fmax(np.fmax(np.fmax(np.fmax(parkinson_pp1,parkinson_pp2),np.fmax(parkinson_pp3, parkinson_pm1)),np.fmax(np.fmax(parkinson_mp1,parkinson_pm2),np.fmax(parkinson_pp4,parkinson_pm3))),parkinson_pp5)
                        agregador_essencial = np.fmax(np.fmax(np.fmax(np.fmax(essencial_pm1,essencial_pm2),np.fmax(essencial_pm3, essencial_pm4)),np.fmax(np.fmax(essencial_pm5,essencial_mp1),np.fmax(essencial_pp1,essencial_pp2))),essencial_pp3)
                        agregador_distonico = np.fmax(np.fmax(np.fmax(np.fmax(distonico_mp1,distonico_pm1),np.fmax(distonico_pp1, distonico_mp2)),np.fmax(np.fmax(distonico_pp2,distonico_mp3),np.fmax(distonico_pp3,distonico_pm2))),distonico_pm3)
                        agregador_funcional = np.fmax(np.fmax(np.fmax(np.fmax(funcional_pm1,funcional_pm2),np.fmax(funcional_pm3, funcional_pp1)),np.fmax(np.fmax(funcional_pp2,funcional_pp3),np.fmax(funcional_pm4,funcional_mp4))),funcional_mp5)
                        agregador_saudavel = np.fmax(np.fmax(np.fmax(np.fmax(saudavel_pm1,saudavel_pp1),np.fmax(saudavel_pm2, saudavel_mp1)),np.fmax(np.fmax(saudavel_pp2,saudavel_pp3),np.fmax(saudavel_pp4,saudavel_pp5))),saudavel_pp6)


                        resultado_parkinson[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_parkinson,'centroid'))
                        resultado_essencial[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_essencial,'centroid'))
                        resultado_distonico[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_distonico,'centroid'))
                        resultado_funcional[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_funcional,'centroid'))
                        resultado_saudavel[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_saudavel,'centroid'))

#Movimento 5


for l in range(0,6):
        for k in range(1,numfiles+1):
                if l==4:
                        
                        parkinson_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[4,k],potencia_nivel_baixo[4,k]),parkinson_baixo)
                        parkinson_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[4,k],potencia_nivel_medio[4,k]),parkinson_baixo)
                        parkinson_pp3 = np.fmin(np.fmin(frequencia_nivel_baixo[4,k],potencia_nivel_alto[4,k]),parkinson_baixo)
                        parkinson_pp4 = np.fmin(np.fmin(frequencia_nivel_medio[4,k],potencia_nivel_baixo[4,k]),parkinson_baixo)
                        parkinson_pm1 = np.fmin(np.fmin(frequencia_nivel_medio[4,k],potencia_nivel_medio[4,k]),parkinson_medio)
                        parkinson_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[4,k],potencia_nivel_alto[4,k]),parkinson_alto)
                        parkinson_pp5 = np.fmin(np.fmin(frequencia_nivel_alto[4,k],potencia_nivel_baixo[4,k]),parkinson_baixo)
                        parkinson_pp6 = np.fmin(np.fmin(frequencia_nivel_alto[4,k],potencia_nivel_medio[4,k]),parkinson_baixo)
                        parkinson_pp7 = np.fmin(np.fmin(frequencia_nivel_alto[4,k],potencia_nivel_alto[4,k]),parkinson_baixo)
                        

                        essencial_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[4,k],potencia_nivel_baixo[4,k]),essencial_baixo)
                        essencial_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[4,k],potencia_nivel_medio[4,k]),essencial_medio)
                        essencial_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[4,k],potencia_nivel_alto[4,k]),essencial_baixo)
                        essencial_pp3 = np.fmin(np.fmin(frequencia_nivel_medio[4,k],potencia_nivel_baixo[4,k]),essencial_baixo)
                        essencial_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[4,k],potencia_nivel_medio[4,k]),essencial_alto)
                        essencial_mp2 = np.fmin(np.fmin(frequencia_nivel_medio[4,k],potencia_nivel_alto[4,k]),essencial_alto)
                        essencial_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[4,k],potencia_nivel_baixo[4,k]),essencial_baixo)
                        essencial_pp5 = np.fmin(np.fmin(frequencia_nivel_alto[4,k],potencia_nivel_medio[4,k]),essencial_baixo)
                        essencial_pp6 = np.fmin(np.fmin(frequencia_nivel_alto[4,k],potencia_nivel_alto[4,k]),essencial_baixo)
                        

                        distonico_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[4,k],potencia_nivel_baixo[4,k]),distonico_baixo)
                        distonico_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[4,k],potencia_nivel_medio[4,k]),distonico_baixo)
                        distonico_pp3 = np.fmin(np.fmin(frequencia_nivel_baixo[4,k],potencia_nivel_alto[4,k]),distonico_baixo)
                        distonico_pm1 = np.fmin(np.fmin(frequencia_nivel_medio[4,k],potencia_nivel_baixo[4,k]),distonico_medio)
                        distonico_pm2 = np.fmin(np.fmin(frequencia_nivel_medio[4,k],potencia_nivel_medio[4,k]),distonico_medio)
                        distonico_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[4,k],potencia_nivel_alto[4,k]),distonico_alto)
                        distonico_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[4,k],potencia_nivel_baixo[4,k]),distonico_baixo)
                        distonico_pm3 = np.fmin(np.fmin(frequencia_nivel_alto[4,k],potencia_nivel_medio[4,k]),distonico_baixo)
                        distonico_pp5 = np.fmin(np.fmin(frequencia_nivel_alto[4,k],potencia_nivel_alto[4,k]),distonico_baixo)
                        

                        funcional_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[4,k],potencia_nivel_baixo[4,k]),funcional_baixo)
                        funcional_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[4,k],potencia_nivel_medio[4,k]),funcional_baixo)
                        funcional_pp3 = np.fmin(np.fmin(frequencia_nivel_baixo[4,k],potencia_nivel_alto[4,k]),funcional_baixo)
                        funcional_pp4 = np.fmin(np.fmin(frequencia_nivel_medio[4,k],potencia_nivel_baixo[4,k]),funcional_baixo)
                        funcional_pm1 = np.fmin(np.fmin(frequencia_nivel_medio[4,k],potencia_nivel_medio[4,k]),funcional_medio)
                        funcional_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[4,k],potencia_nivel_alto[4,k]),funcional_alto)
                        funcional_pp5 = np.fmin(np.fmin(frequencia_nivel_alto[4,k],potencia_nivel_baixo[4,k]),funcional_baixo)
                        funcional_pp6 = np.fmin(np.fmin(frequencia_nivel_alto[4,k],potencia_nivel_medio[4,k]),funcional_baixo)
                        funcional_pm2 = np.fmin(np.fmin(frequencia_nivel_alto[4,k],potencia_nivel_alto[4,k]),funcional_medio)
                        

                        saudavel_mp1 = np.fmin(np.fmin(frequencia_nivel_baixo[4,k],potencia_nivel_baixo[4,k]),saudavel_alto)
                        saudavel_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[4,k],potencia_nivel_medio[4,k]),saudavel_baixo)
                        saudavel_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[4,k],potencia_nivel_alto[4,k]),saudavel_baixo)
                        saudavel_mp2 = np.fmin(np.fmin(frequencia_nivel_medio[4,k],potencia_nivel_baixo[4,k]), saudavel_alto)
                        saudavel_pm1 = np.fmin(np.fmin(frequencia_nivel_medio[4,k],potencia_nivel_medio[4,k]),saudavel_medio)
                        saudavel_pp3 = np.fmin(np.fmin(frequencia_nivel_medio[4,k],potencia_nivel_alto[4,k]),saudavel_baixo)
                        saudavel_mp3 = np.fmin(np.fmin(frequencia_nivel_alto[4,k],potencia_nivel_baixo[4,k]),saudavel_alto)
                        saudavel_pm2 = np.fmin(np.fmin(frequencia_nivel_alto[4,k],potencia_nivel_medio[4,k]),saudavel_medio)
                        saudavel_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[4,k],potencia_nivel_alto[4,k]),saudavel_baixo)


                        agregador_parkinson = np.fmax(np.fmax(np.fmax(np.fmax(parkinson_pp1,parkinson_pp2),np.fmax(parkinson_pp3, parkinson_pp4)),np.fmax(np.fmax(parkinson_pm1,parkinson_mp1),np.fmax(parkinson_pp5,parkinson_pp6))),parkinson_pp7)
                        agregador_essencial = np.fmax(np.fmax(np.fmax(np.fmax(essencial_pp1,parkinson_pm1),np.fmax(essencial_pp2, essencial_pp3)),np.fmax(np.fmax(essencial_mp1,essencial_mp2),np.fmax(essencial_pp4,essencial_pp5))),essencial_pp6)
                        agregador_distonico = np.fmax(np.fmax(np.fmax(np.fmax(distonico_pp1,distonico_pp2),np.fmax(distonico_pp3, distonico_pm1)),np.fmax(np.fmax(distonico_pm2,distonico_mp1),np.fmax(distonico_pp4,distonico_pm3))),distonico_pp5)
                        agregador_funcional = np.fmax(np.fmax(np.fmax(np.fmax(funcional_pp1,funcional_pp2),np.fmax(funcional_pp3, funcional_pp4)),np.fmax(np.fmax(funcional_pm1,funcional_mp1),np.fmax(funcional_pp5,funcional_pp6))),funcional_pm2)
                        agregador_saudavel = np.fmax(np.fmax(np.fmax(np.fmax(saudavel_mp1,saudavel_pp1),np.fmax(saudavel_pp2, saudavel_mp2)),np.fmax(np.fmax(saudavel_pm1,saudavel_pp3),np.fmax(saudavel_mp3,saudavel_pm2))),saudavel_pp4)


                        resultado_parkinson[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_parkinson,'centroid'))
                        resultado_essencial[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_essencial,'centroid'))
                        resultado_distonico[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_distonico,'centroid'))
                        resultado_funcional[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_funcional,'centroid'))
                        resultado_saudavel[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_saudavel,'centroid'))

#Movimento 6

for l in range(0,6):
        for k in range(1,numfiles+1):
                if l==5:
                        parkinson_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[5,k],potencia_nivel_baixo[5,k]),parkinson_baixo)
                        parkinson_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[5,k],potencia_nivel_medio[5,k]),parkinson_baixo)
                        parkinson_pp3 = np.fmin(np.fmin(frequencia_nivel_baixo[5,k],potencia_nivel_alto[5,k]),parkinson_baixo)
                        parkinson_pm1 = np.fmin(np.fmin(frequencia_nivel_medio[5,k],potencia_nivel_baixo[5,k]),parkinson_medio)
                        parkinson_pm2 = np.fmin(np.fmin(frequencia_nivel_medio[5,k],potencia_nivel_medio[5,k]),parkinson_medio)
                        parkinson_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[5,k],potencia_nivel_alto[5,k]),parkinson_alto)
                        parkinson_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[5,k],potencia_nivel_baixo[5,k]),parkinson_baixo)
                        parkinson_pp5 = np.fmin(np.fmin(frequencia_nivel_alto[5,k],potencia_nivel_medio[5,k]),parkinson_baixo)
                        parkinson_pp6 = np.fmin(np.fmin(frequencia_nivel_alto[5,k],potencia_nivel_alto[5,k]),parkinson_baixo)
                        

                        essencial_pm1 = np.fmin(np.fmin(frequencia_nivel_baixo[5,k],potencia_nivel_baixo[5,k]),essencial_medio)
                        essencial_pm2 = np.fmin(np.fmin(frequencia_nivel_baixo[5,k],potencia_nivel_medio[5,k]),essencial_medio)
                        essencial_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[5,k],potencia_nivel_alto[5,k]),essencial_baixo)
                        essencial_pm3 = np.fmin(np.fmin(frequencia_nivel_medio[5,k],potencia_nivel_baixo[5,k]),essencial_medio)
                        essencial_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[5,k],potencia_nivel_medio[5,k]),essencial_alto)
                        essencial_mp2 = np.fmin(np.fmin(frequencia_nivel_medio[5,k],potencia_nivel_alto[5,k]),essencial_alto)
                        essencial_pp2 = np.fmin(np.fmin(frequencia_nivel_alto[5,k],potencia_nivel_baixo[5,k]),essencial_baixo)
                        essencial_pp3 = np.fmin(np.fmin(frequencia_nivel_alto[5,k],potencia_nivel_medio[5,k]),essencial_baixo)
                        essencial_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[5,k],potencia_nivel_alto[5,k]),essencial_baixo)
                        

                        distonico_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[5,k],potencia_nivel_baixo[5,k]),distonico_baixo)
                        distonico_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[5,k],potencia_nivel_medio[5,k]),distonico_baixo)
                        distonico_pp3 = np.fmin(np.fmin(frequencia_nivel_baixo[5,k],potencia_nivel_alto[5,k]),distonico_baixo)
                        distonico_pm1 = np.fmin(np.fmin(frequencia_nivel_medio[5,k],potencia_nivel_baixo[5,k]), distonico_medio)
                        distonico_pm2 = np.fmin(np.fmin(frequencia_nivel_medio[5,k],potencia_nivel_medio[5,k]),distonico_medio)
                        distonico_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[5,k],potencia_nivel_alto[5,k]),distonico_alto)
                        distonico_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[5,k],potencia_nivel_baixo[5,k]),distonico_baixo)
                        distonico_mp2 = np.fmin(np.fmin(frequencia_nivel_alto[5,k],potencia_nivel_medio[5,k]),distonico_alto)
                        distonico_pm3 = np.fmin(np.fmin(frequencia_nivel_alto[5,k],potencia_nivel_alto[5,k]),distonico_medio)
                        

                        funcional_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[5,k],potencia_nivel_baixo[5,k]),funcional_baixo)
                        funcional_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[5,k],potencia_nivel_medio[5,k]),funcional_baixo)
                        funcional_pp3 = np.fmin(np.fmin(frequencia_nivel_baixo[5,k],potencia_nivel_alto[5,k]),funcional_baixo)
                        funcional_pp4 = np.fmin(np.fmin(frequencia_nivel_medio[5,k],potencia_nivel_baixo[5,k]),funcional_baixo)
                        funcional_pm1 = np.fmin(np.fmin(frequencia_nivel_medio[5,k],potencia_nivel_medio[5,k]),funcional_medio)
                        funcional_mp1 = np.fmin(np.fmin(frequencia_nivel_medio[5,k],potencia_nivel_alto[5,k]),funcional_alto)
                        funcional_pp5 = np.fmin(np.fmin(frequencia_nivel_alto[5,k],potencia_nivel_baixo[5,k]),funcional_baixo)
                        funcional_pm2 = np.fmin(np.fmin(frequencia_nivel_alto[5,k],potencia_nivel_medio[5,k]),funcional_medio)
                        funcional_mp2 = np.fmin(np.fmin(frequencia_nivel_alto[5,k],potencia_nivel_alto[5,k]),funcional_alto)
                        

                        saudavel_mp1 = np.fmin(np.fmin(frequencia_nivel_baixo[5,k],potencia_nivel_baixo[5,k]),saudavel_alto)
                        saudavel_pp1 = np.fmin(np.fmin(frequencia_nivel_baixo[5,k],potencia_nivel_medio[5,k]),saudavel_baixo)
                        saudavel_pp2 = np.fmin(np.fmin(frequencia_nivel_baixo[5,k],potencia_nivel_alto[5,k]),saudavel_baixo)
                        saudavel_mp2 = np.fmin(np.fmin(frequencia_nivel_medio[5,k],potencia_nivel_baixo[5,k]), saudavel_alto)
                        saudavel_pm1 = np.fmin(np.fmin(frequencia_nivel_medio[5,k],potencia_nivel_medio[5,k]),saudavel_medio)
                        saudavel_pp3 = np.fmin(np.fmin(frequencia_nivel_medio[5,k],potencia_nivel_alto[5,k]),saudavel_baixo)
                        saudavel_pm2 = np.fmin(np.fmin(frequencia_nivel_alto[5,k],potencia_nivel_baixo[5,k]),saudavel_medio)
                        saudavel_pm3 = np.fmin(np.fmin(frequencia_nivel_alto[5,k],potencia_nivel_medio[5,k]),saudavel_medio)
                        saudavel_pp4 = np.fmin(np.fmin(frequencia_nivel_alto[5,k],potencia_nivel_alto[5,k]),saudavel_baixo)


                        agregador_parkinson = np.fmax(np.fmax(np.fmax(np.fmax(parkinson_pp1,parkinson_pp2),np.fmax(parkinson_pp3, parkinson_pm1)),np.fmax(np.fmax(parkinson_pm2,parkinson_mp1),np.fmax(parkinson_pp4,parkinson_pp5))),parkinson_pp6)
                        agregador_essencial = np.fmax(np.fmax(np.fmax(np.fmax(essencial_pm1,parkinson_pm2),np.fmax(essencial_pp1, essencial_pm3)),np.fmax(np.fmax(essencial_mp1,essencial_mp2),np.fmax(essencial_pp2,essencial_pp3))),essencial_pp4)
                        agregador_distonico = np.fmax(np.fmax(np.fmax(np.fmax(distonico_pp1,distonico_pp2),np.fmax(distonico_pp3, distonico_pm1)),np.fmax(np.fmax(distonico_pm2,distonico_mp1),np.fmax(distonico_pp4,distonico_mp2))),distonico_pm3)
                        agregador_funcional = np.fmax(np.fmax(np.fmax(np.fmax(funcional_pp1,funcional_pp2),np.fmax(funcional_pp3, funcional_pp4)),np.fmax(np.fmax(funcional_pm1,funcional_mp1),np.fmax(funcional_pp5,funcional_pm2))),funcional_mp2)
                        agregador_saudavel = np.fmax(np.fmax(np.fmax(np.fmax(saudavel_mp1,saudavel_pp1),np.fmax(saudavel_pp2, saudavel_mp2)),np.fmax(np.fmax(saudavel_pm1,saudavel_pp3),np.fmax(saudavel_pm2,saudavel_pm3))),saudavel_pp4)
                        

                        resultado_parkinson[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_parkinson,'centroid'))
                        resultado_essencial[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_essencial,'centroid'))
                        resultado_distonico[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_distonico,'centroid'))
                        resultado_funcional[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_funcional,'centroid'))
                        resultado_saudavel[l][k] = 2*(fuzzy.defuzz(porcentagem,agregador_saudavel,'centroid'))
                        


for k in range(1,numfiles+1):
        
        #probabilidade_parkinson = np.mean(resultado_parkinson[:,k])
        #probabilidade_essencial = np.mean(resultado_essencial[:,k])
        #probabilidade_distonico = np.mean(resultado_distonico[:,k])
        #probabilidade_funcional = np.mean(resultado_funcional[:,k])
        #probabilidade_saudavel = np.mean(resultado_saudavel[:,k])

        #print(probabilidade_parkinson)
        #print(probabilidade_essencial)
        #print(probabilidade_distonico)
        #rint(probabilidade_funcional)
        #print(probabilidade_saudavel)

        parkinson = 0
        essencial = 0
        distonico = 0
        funcional = 0
        saudavel = 0
        
        for l in range(0,6):
                
                if (resultado_parkinson[l][k] >= resultado_essencial[l][k] and resultado_parkinson[l][k] >= resultado_distonico[l][k] and resultado_parkinson[l][k] >= resultado_funcional[l][k] and resultado_parkinson[l][k] >= resultado_saudavel[l][k]):
                        parkinson = parkinson + resultado_parkinson[l][k]
                elif (resultado_essencial[l][k] >= resultado_parkinson[l][k] and resultado_essencial[l][k] >= resultado_distonico[l][k] and resultado_essencial[l][k] >= resultado_funcional[l][k] and resultado_essencial[l][k] >= resultado_saudavel[l][k]):
                        essencial = essencial + resultado_essencial[l][k]
                elif (resultado_distonico[l][k] >= resultado_parkinson[l][k] and resultado_distonico[l][k] >= resultado_essencial[l][k] and resultado_distonico[l][k] >= resultado_funcional[l][k] and resultado_distonico[l][k] >= resultado_saudavel[l][k]):
                        distonico = distonico + resultado_distonico[l][k]
                elif (resultado_funcional[l][k] >= resultado_parkinson[l][k] and resultado_funcional[l][k] >= resultado_essencial[l][k] and resultado_funcional[l][k] >= resultado_distonico[l][k] and resultado_funcional[l][k] >= resultado_saudavel[l][k]):
                        funcional = funcional + resultado_funcional[l][k]
                elif (resultado_saudavel[l][k] >= resultado_parkinson[l][k] and resultado_saudavel[l][k] >= resultado_essencial[l][k] and resultado_saudavel[l][k] >= resultado_distonico[l][k] and resultado_saudavel[l][k] >= resultado_funcional[l][k]):
                        saudavel = saudavel + resultado_saudavel[l][k]*0.51
                        
        probabilidade_parkinson = parkinson/6
        probabilidade_essencial = essencial/6
        probabilidade_distonico = distonico/6
        probabilidade_funcional = funcional/6
        probabilidade_saudavel = saudavel/6


        if (35 >= probabilidade_parkinson and 35 >= probabilidade_essencial and 35 >= probabilidade_distonico and 35 >= probabilidade_funcional and 35 >= probabilidade_saudavel):
                 print('O voluntário ',k,' pertence ao grupo "Outros".')
                        
        elif (probabilidade_parkinson > probabilidade_essencial and probabilidade_parkinson > probabilidade_distonico and probabilidade_parkinson > probabilidade_funcional and probabilidade_parkinson > probabilidade_saudavel):
                print('O voluntário ',k,' pertence ao grupo "Parkinson", uma vez que a sua probabilidade de pertencer a tal grupo é de ',probabilidade_parkinson)
                        
        elif (probabilidade_essencial > probabilidade_parkinson and probabilidade_essencial > probabilidade_distonico and probabilidade_essencial > probabilidade_funcional and probabilidade_essencial > probabilidade_saudavel):
                print('O voluntário ',k,' pertence ao grupo "Essencial", uma vez que a sua probabilidade de pertencer a tal grupo é de ',probabilidade_essencial)
                        
        elif (probabilidade_distonico > probabilidade_parkinson and probabilidade_distonico > probabilidade_essencial and probabilidade_distonico > probabilidade_funcional and probabilidade_distonico > probabilidade_saudavel):
                print('O voluntário ',k,' pertence ao grupo "Distônico", uma vez que a sua probabilidade de pertencer a tal grupo é de ',probabilidade_distonico)
                        
        elif (probabilidade_funcional > probabilidade_parkinson and probabilidade_funcional > probabilidade_essencial and probabilidade_funcional > probabilidade_distonico and probabilidade_funcional > probabilidade_saudavel):
                print('O voluntário ',k,' pertence ao grupo "Funcional", uma vez que a sua probabilidade de pertencer a tal grupo é de ',probabilidade_funcional)
                        
        elif (probabilidade_saudavel > probabilidade_parkinson and probabilidade_saudavel > probabilidade_essencial and probabilidade_saudavel > probabilidade_distonico and probabilidade_saudavel > probabilidade_funcional):
                print('O voluntário ',k,' pertence ao grupo "Saudável", uma vez que a sua probabilidade de pertencer a tal grupo é de ',probabilidade_saudavel)
                



            #plt.plot(f[l,k],PSD[l,k])
            #plt.axis(v)
            #plt.show()



#for l in range(0,6):
#
#        for k in range(1,11):
#            plt.title('Movimento %s' %Movimento[l])
#            plt.plot(f[l,k],PSD[l,k],label = 'Voluntário %s' %k)
#            plt.axis(v)
#            plt.legend()
#            print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
#        plt.show()

       # for k in range(11,21):
            #plt.title('Movimento %s' %Movimento[l])
           # plt.plot(f[l,k],PSD[l,k],label = 'Voluntário %s' %k)
          #  plt.axis(v)
         #   plt.legend()
        #    print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
       # plt.show()
      #  for k in range(21,31):
            #plt.title('Movimento %s' %Movimento[l])
            #plt.plot(f[l,k],PSD[l,k],label = 'Voluntário %s' %k)
           # plt.axis(v)
          #  plt.legend()
         #   print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
        #plt.show()
        #for k in range(31,41):
            #plt.title('Movimento %s' %Movimento[l])
            # plt.axis(v)
          #  plt.legend()
         #   print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
        #plt.show()
       # for k in range(41,54):
      #      plt.title('Movimento %s' %Movimento[l])
     #       plt.plot(f[l,k],PSD[l,k],label = 'Voluntário %s' %k)
    #        plt.axis(v)
   #         plt.legend()
  #          print('A frequência de pico para o movimento ',movimento[l],' do voluntário ',k,' é ',frequencia_pico[l,k],'. Já a potênica de pico correspondente é ', potencia_pico[l,k])
 #       plt.show()
