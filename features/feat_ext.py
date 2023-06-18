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
def get_matrix_f0(filename, n_frames = 97):
    a = Sinal(filename)
    a.carrega()
    a.pitch()
    mediaF0 = [a.meanF0] * n_frames
    desvioF0 = [a.stdevF0] * n_frames
    minimoF0 = [a.minF0] * n_frames
    maximoF0 = [a.maxF0] * n_frames
    range_F0 = [a.rangeF0] * n_frames

    return mediaF0, desvioF0, minimoF0, maximoF0, range_F0

def get_matrix_jitter(filename, n_frames = 97):
    a = Sinal(filename)
    a.carrega()
    a.jitter()
    mediaJitter = [a.jitt] * n_frames

    return mediaJitter

def get_matrix_shimmer(filename, n_frames = 97):
    a = Sinal(filename)
    a.carrega()
    a.shimmer()
    mediaShimmer = [a.shimm] * n_frames

    return mediaShimmer

def get_matrix_hnr(filename, n_frames = 97):
    a = Sinal(filename)
    a.carrega()
    a.getHNR()
    mediaHNR = [a.hnr] * n_frames

    return mediaHNR

def get_matrix_gne(filename, n_frames = 97):
    a = Sinal(filename)
    a.carrega()
    a.getGNE()
    mediaGNE = [a.gne] * n_frames

    return mediaGNE

def get_matrix_f1(filename, n_frames = 97):
    a = Sinal(filename)
    a.carrega()
    a.getFormants()
    mediaF1 = [a.meanF1] * n_frames
    desvioF1 = [a.stdevF1] * n_frames
    minimoF1 = [a.minF1] * n_frames
    maximoF1 = [a.maxF1] * n_frames
    range_F1 = [a.rangeF1] * n_frames

    return mediaF1, desvioF1, minimoF1, maximoF1, range_F1

def get_matrix_f2(filename, n_frames = 97):
    a = Sinal(filename)
    a.carrega()
    a.getFormants()
    mediaF2 = [a.meanF2] * n_frames
    desvioF2 = [a.stdevF2] * n_frames
    minimoF2 = [a.minF2] * n_frames
    maximoF2 = [a.maxF2] * n_frames
    range_F2 = [a.rangeF2] * n_frames

    return mediaF2, desvioF2, minimoF2, maximoF2, range_F2

def get_matrix_f3(filename, n_frames = 97):
    a = Sinal(filename)
    a.carrega()
    a.getFormants()
    mediaF3 = [a.meanF3] * n_frames
    desvioF3 = [a.stdevF3] * n_frames
    minimoF3 = [a.minF3] * n_frames
    maximoF3 = [a.maxF3] * n_frames
    range_F3 = [a.rangeF3] * n_frames

    return mediaF3, desvioF3, minimoF3, maximoF3, range_F3

def get_matrix_cpps(filename, n_frames = 97):
    a = Sinal(filename)
    a.carrega()
    a.getCPPS()
    mediaCPPS = [a.cpps] * n_frames

    return mediaCPPS

def get_matrix_slope(filename, n_frames = 97):
    a = Sinal(filename)
    a.carrega()
    a.getSlope()
    mediaSlope = [a.slope] * n_frames

    return mediaSlope