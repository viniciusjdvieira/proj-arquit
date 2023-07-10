import numpy as np
import soundfile as sf
import pandas as pd
import tensorflow as tf
from feat_ext import get_lpc, get_matrix_cpps, get_matrix_slope


def get_probs(path_sinal, path_modelo):
    '''
    Esta função carrega um sinal, e responde a sua probabilidade de
    ser saudável ou patológico
    '''
    # carregando o sinal
    data, samplerate = sf.read(path_sinal)

    if len(data.shape) > 1:
        if np.shape(data)[0] > np.shape(data)[1]:
            data = np.mean(data, axis=1)
        else:
            data = np.mean(data, axis=0)

    # criando o dataframe para receber as métricas
    df = pd.DataFrame()

    # extraindo LPCs
    media_lpcs, lpcs = get_lpc(data, order = 29)
    n_seg = np.shape(lpcs)[0]

    # extraindo cpps
    cpps = get_matrix_cpps(path_sinal, n_frames = n_seg)

    # extraindo slope
    slope = get_matrix_slope(path_sinal, n_frames = n_seg)

    # atribuindo as métricas ao dataframe
    df['cpps'] = cpps
    df['slope'] = slope
    df = pd.concat([df, pd.DataFrame(lpcs,columns=['lpc1','lpc2','lpc3','lpc4','lpc5','lpc6',
                                                   'lpc7','lpc8','lpc9','lpc10','lpc11','lpc12',
                                                   'lpc13','lpc14','lpc15','lpc16','lpc17','lpc18',
                                                   'lpc19','lpc20','lpc21','lpc22','lpc23','lpc24',
                                                   'lpc25','lpc26','lpc27','lpc28','lpc29'])], axis=1)
    
    # ajustando dataframe para colocar como tensor
    numeric_feature_names = ['cpps', 'slope','lpc1',  'lpc2',
                         'lpc3', 'lpc4', 'lpc5', 'lpc6',
                         'lpc7', 'lpc8','lpc9', 'lpc10',
                         'lpc11', 'lpc12']
    numeric_features = df[numeric_feature_names]

    # convertendo features para TENSOR
    tf.convert_to_tensor(numeric_features)

    # Aplicando normalização das features (para equalizar grandezas)]
    normalizer = tf.keras.layers.Normalization(axis=-1)
    normalizer.adapt(numeric_features)

    # Carregue o modelo
    modelo_carregado = tf.keras.models.load_model(path_modelo)

    # predições
    predictions = modelo_carregado.predict(numeric_features)
    predicted_classes = (predictions > 0.5).astype(int)
    pred_vec = np.reshape(predicted_classes, len(predicted_classes))
    contagem = np.bincount(pred_vec)

    # avaliando probabilidades
    if len(contagem.shape) > 1:
       prob_sdl = ( contagem[0] / len(pred_vec)) * 100
       prob_ptl = ( contagem[1] / len(pred_vec)) * 100
    elif len(contagem.shape) == 1:
        if pred_vec[0] == 0:
          prob_sdl = 100
          prob_ptl = 0
        else:
           prob_sdl = 0
           prob_ptl = 100
    else:
        pass

    return prob_sdl , prob_ptl