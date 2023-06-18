import numpy as np
import librosa
import soundfile as sf
from praat_class import Sinal

##----------------------------------------------------
# extrator de features
##----------------------------------------------------

## LPCS
def get_lpc(signal, order = 12, sr = 25000,
             frame_length = 512, hop_length = 256):
    '''
    função para extrair LPCs
    
    retorna um vetor de média sobre frames
    e a matrix para todos os frames
    '''
    ordem = (sr // 1000) + 4
    window = np.hamming(frame_length)
    last_sf = len(signal) - frame_length
    ff = []
    for start in range(0, last_sf + 1, hop_length):
        end_sf = start + frame_length
        fi = signal[start : end_sf]
        fi_w = fi * window
        f_lpc = librosa.lpc(fi_w, order = ordem)
        ff.append(f_lpc[1:])

    media_lpc = np.nanmean(ff, axis = 0)
    lpcs = ff

    return media_lpc , lpcs


## MFCCs
def get_mfcc(signal, sr = 25000, order = 12,
              frame_length = 512, hop_length = 256):
    ''' 
    função para calcular MFCCs
    
    '''
    coeffs = librosa.feature.mfcc(signal, n_mfcc = order, 
                                  sr = sr,
                                  n_fft = frame_length,
                                  hop_length = hop_length,
                                  window = 'hamming')
    
    media_coeffs = np.nanmean(coeffs, axis = 1)

    return media_coeffs, coeffs.T


## delta-MFCCs
def get_delta_mfcc(signal, sr = 25000, order = 12,
                    frame_length = 512, hop_length = 256):
    ''' 
    função para calcular delta-MFCCs
    
    '''
    coeffs = librosa.feature.mfcc(signal, n_mfcc = order, 
                                  sr = sr,
                                  n_fft = frame_length,
                                  hop_length = hop_length,
                                  window = 'hamming')
    
    delta_coeffs = librosa.feature.delta(coeffs, order=1)
    
    media_coeffs = np.nanmean(delta_coeffs, axis = 1)

    return media_coeffs, delta_coeffs.T


## delta-delta-MFCCs
def get_delta_delta_mfcc(signal, sr = 25000, order = 12, frame_length = 512, hop_length = 256):
    ''' 
    função para calcular delta-MFCCs
    
    '''
    coeffs = librosa.feature.mfcc(signal, n_mfcc = order, 
                                  sr = sr,
                                  n_fft = frame_length,
                                  hop_length = hop_length,
                                  window = 'hamming')
    
    delta_delta_coeffs = librosa.feature.delta(coeffs, order=2)
    
    media_coeffs = np.nanmean(delta_delta_coeffs, axis = 1)

    return media_coeffs, delta_delta_coeffs.T

## Repetindo features do praat para matriz
