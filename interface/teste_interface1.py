import tkinter as tk

# Cria a janela principal
janela = tk.Tk()

# Define o título da janela
janela.title("Minha Interface Gráfica")

# Cria um rótulo na janela
rotulo = tk.Label(janela, text="Olá, mundo!")
rotulo.pack()

# Executa o loop principal da aplicação
janela.mainloop()
