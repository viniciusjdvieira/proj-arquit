import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram
import numpy as np


def iniciar_gravacao():
    frames = []  # Inicializar a lista de frames de áudio

    def callback(indata, frames, time, status):
        frames.append(indata.copy())

    messagebox.showinfo("Gravação", "A gravação começará em breve. Clique em OK e fale durante 5 segundos.")
    with sd.InputStream(callback=callback, channels=1):
        sd.sleep(int(duration * 1000))

    # Verificar se existem frames de áudio gravados
    if frames:
        arquivo_audio = "gravacao.wav"
        sf.write(arquivo_audio, np.concatenate(frames), samplerate)

        # Exibe a janela com a opção de reproduzir novamente ou prosseguir
        escolha = messagebox.askquestion("Gravação Concluída",
                                         "A gravação foi concluída. Deseja reproduzir novamente?")
        if escolha == 'yes':
            reproduzir_audio(arquivo_audio)
        else:
            exibir_espectrograma(arquivo_audio)
    else:
        messagebox.showwarning("Gravação Vazia", "Nenhum áudio foi gravado.")


def reproduzir_audio(arquivo_audio):
    data, fs = sf.read(arquivo_audio, dtype='float32')
    sd.play(data, fs)
    sd.wait()


def exibir_espectrograma(arquivo_audio):
    fs, audio = wavfile.read(arquivo_audio)
    f, t, Sxx = spectrogram(audio, fs)
    plt.pcolormesh(t, f, 10 * np.log10(Sxx))
    plt.xlabel('Tempo [s]')
    plt.ylabel('Frequência [Hz]')
    plt.colorbar(label='Intensidade [dB]')
    plt.title('Espectrograma do áudio gravado')
    plt.show()


def entrar():
    nome = entry_nome.get()
    matricula = entry_matricula.get()
    if nome and matricula:
        janela_inicial.destroy()
        janela_gravacao = tk.Toplevel()
        janela_gravacao.title("Gravação de Áudio")

        label_instrucao = tk.Label(janela_gravacao, text="Pressione o botão 'Gravar' e fale durante 5 segundos.")
        label_instrucao.pack()

        button_gravar = tk.Button(janela_gravacao, text="Gravar", command=iniciar_gravacao)
        button_gravar.pack()

        janela_gravacao.mainloop()
    else:
        messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos antes de prosseguir.")


# Configurações iniciais
samplerate = 44100
duration = 5

# Cria a janela inicial
janela_inicial = tk.Tk()
janela_inicial.title("Bem-vindo!")

# Adiciona a imagem
imagem = tk.PhotoImage(file=r"D:\Documentos_HDD\013_postdocIFPB\Artigo_submission_abril2023\pos acceptance\final_files\LaTex_content_vieira\logo.png")
label_imagem = tk.Label(janela_inicial, image=imagem)
label_imagem.pack()

# Adiciona a mensagem de boas-vindas
label_boas_vindas = tk.Label(janela_inicial, text="Bem-vindo! Por favor, informe seu nome e matrícula.")
label_boas_vindas.pack()

# Adiciona os campos para nome e matrícula
label_nome = tk.Label(janela_inicial, text="Nome:")
label_nome.pack()
entry_nome = tk.Entry(janela_inicial)
entry_nome.pack()

label_matricula = tk.Label(janela_inicial, text="Matrícula:")
label_matricula.pack()
entry_matricula = tk.Entry(janela_inicial)
entry_matricula.pack()

# Adiciona o botão de entrada
button_entrar = tk.Button(janela_inicial, text="ENTER", command=entrar)
button_entrar.pack()

# Executa o loop principal da aplicação
janela_inicial.mainloop()
