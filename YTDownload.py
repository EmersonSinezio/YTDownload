import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp

# Função para baixar vídeo ou áudio
def baixar_midia(link, pasta_destino, tipo, label_resultado):
    def progress_hook(d):
        # Atualiza o label durante o download
        if d['status'] == 'downloading':
            label_resultado.config(text="Download sendo feito...", bg="yellow", fg="black")
            root.update_idletasks()  # Atualiza a interface gráfica
        elif d['status'] == 'finished':
            label_resultado.config(text="Download concluído!", bg="green")
            root.update_idletasks()

    if tipo == 'Vídeo':
        ydl_opts = {
            'format': 'best',  # Baixa o melhor formato disponível
            'outtmpl': f'{pasta_destino}/%(title)s.%(ext)s',  # Define o diretório de saída
            'progress_hooks': [progress_hook],  # Função para acompanhar o progresso
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',  # Converte para o formato desejado
                'preferedformat': 'mp4',  # Formato desejado
            }],
        }
    else:  # Áudio
        ydl_opts = {
            'format': 'bestaudio/best',  # Baixa o melhor áudio disponível
            'outtmpl': f'{pasta_destino}/%(title)s.%(ext)s',  # Define o diretório de saída
            'progress_hooks': [progress_hook],  # Função para acompanhar o progresso
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Extrai o áudio
                'preferredcodec': 'mp3',  # Codec desejado
                'preferredquality': '192',  # Qualidade desejada
            }],
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            return f"Baixado com sucesso!\n'{info['title']}'"
    except Exception as e:
        return f"Erro ao baixar o {tipo.lower()}: {e}"

# Função para abrir a caixa de diálogo para selecionar a pasta de destino
def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        entry_pasta.delete(0, tk.END)  # Limpa o campo
        entry_pasta.insert(0, pasta)  # Preenche com o caminho selecionado

# Função que será chamada quando o botão 'Baixar' for pressionado
def iniciar_download():
    link = entry_link.get()
    pasta_destino = entry_pasta.get()
    tipo = 'Vídeo' if var_tipo.get() == 1 else 'Áudio'
    
    if link and pasta_destino:
        label_resultado.config(text="Baixando... Aguarde!", bg="yellow", fg="black")
        root.update_idletasks()  # Atualiza a interface
        mensagem = baixar_midia(link, pasta_destino, tipo, label_resultado)
        label_resultado.config(text=mensagem, bg="green" if "sucesso" in mensagem else "red")
    else:
        messagebox.showwarning("Campos inválidos", "Por favor, insira um link e escolha uma pasta de destino.")

# Criando a janela principal
root = tk.Tk()
root.title("Youtube Downloader")
root.geometry("700x300")

# Layout
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Link do YouTube
label_link = tk.Label(frame, text="Insira o link do YouTube:")
label_link.grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_link = tk.Entry(frame, width=50)
entry_link.grid(row=0, column=1, padx=5, pady=5)

# Pasta de destino
label_pasta = tk.Label(frame, text="Escolha a pasta de destino:")
label_pasta.grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_pasta = tk.Entry(frame, width=50)
entry_pasta.grid(row=1, column=1, padx=5, pady=5)
botao_pasta = tk.Button(frame, text="Procurar", command=escolher_pasta)
botao_pasta.grid(row=1, column=2, padx=5, pady=5)

# Tipo de mídia (Vídeo ou Áudio)
var_tipo = tk.IntVar()
radio_video = tk.Radiobutton(frame, text="Vídeo", variable=var_tipo, value=1)
radio_video.grid(row=2, column=0, padx=5, pady=5)
radio_audio = tk.Radiobutton(frame, text="Áudio", variable=var_tipo, value=2)
radio_audio.grid(row=2, column=1, padx=5, pady=5)

# Botão para iniciar o download
botao_download = tk.Button(frame, text="Baixar", command=iniciar_download, width="20")
botao_download.grid(row=3, column=0, columnspan=3, pady=10)

# Label para mostrar a mensagem de status
label_resultado = tk.Label(root, text="", fg="white", height=2)
label_resultado.pack(pady=10)

# Inicia a interface
root.mainloop()
