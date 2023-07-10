import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import soundfile as sf 
from matplotlib import rc, font_manager

def plot_signal_spec(filename):

    # leitura do sinal
    xT,Fs=sf.read(filename)
    Ts=1/Fs # Período de amostragem
    Nx=len(xT)
    t=(np.arange(Nx))/Fs
    # pegando entre o primeiro e o quarto segundo do sinal
    xT1=xT[22050:-22050]
    Nx1=len(xT1)
    t1=(np.arange(Nx1))/Fs

    # Espectrograma
    Lx=round(0.02*Fs)
    ff, tt, Sxx = signal.spectrogram(xT1,Fs,window='hamming',nperseg=Lx,noverlap=Lx/2,mode='psd')
    sg_db = 10 * np.log10(Sxx)


    fig, axs = plt.subplots(2, 1, figsize=(10,4))
    axs[0].plot(t1,xT1,'b')
    axs[0].set_xlabel('Tempo (s)', fontsize=10)
    axs[0].set_ylabel('Amplitude', fontsize=10)
    axs[1].pcolormesh(tt, ff, sg_db, shading='gouraud',cmap='rainbow')
    axs[1].set_xlabel('Tempo (s)', fontsize=10)
    axs[1].set_ylabel('Freq. (Hz)', fontsize=10)
    axs[1].set( ylim=(0, 5000))

    # set the spacing between subplots
    plt.subplots_adjust(left=0.16,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.35)
    
    return fig