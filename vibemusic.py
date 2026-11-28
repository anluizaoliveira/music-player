import os
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pygame import mixer
from pygame import error as pygame_error
from mutagen import File as MutagenFile

# ==========================================
# 1. CONFIGURAÇÕES E CORES
# ==========================================

COR_FUNDO = "#E9DDFB"
COR_TEXTO = "#30213F"
COR_ROXO = "#B58AE8"
COR_PAINEL = "#D8C5F2"
COR_SUPERFICIE = "#CBB2EA"
COR_DESTAQUE = "#7041A6"

# ==========================================
# 2. INICIALIZAÇÃO DA JANELA
# ==========================================

mixer.init()

janela = tk.Tk()
janela.title("VYBE | Music Player")
janela.geometry("352x255")
janela.configure(bg=COR_FUNDO)
janela.resizable(False, False)


# ==========================================
# 3. CRIAÇÃO DOS FRAMES
# ==========================================

frame_esquerda = tk.Frame(
    janela,
    width=150,
    height=150,
    bg=COR_PAINEL,
    relief="flat"
)
frame_esquerda.grid(
    row=0,
    column=0,
    pady=1,
    padx=1,
    sticky="nsew"
)

frame_direita = tk.Frame(
    janela,
    width=200,
    height=150,
    bg=COR_PAINEL,
    relief="flat"
)
frame_direita.grid(
    row=0,
    column=1,
    pady=1,
    padx=1,
    sticky="nsew"
)

frame_baixo = tk.Frame(
    janela,
    width=352,
    height=100,
    bg=COR_PAINEL,
    relief="flat"
)
frame_baixo.grid(
    row=1,
    column=0,
    columnspan=2,
    pady=1,
    padx=1,
    sticky="nsew"
)

# Impede que os frames mudem de tamanho
frame_esquerda.grid_propagate(False)
frame_direita.grid_propagate(False)
frame_baixo.grid_propagate(False)


# ==========================================
# 4. CARREGAMENTO DO LOGOTIPO
# ==========================================

PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))

img_logo_original = Image.open(
    os.path.join(PASTA_PROJETO, "icon1.png.png")
)
img_logo_original = img_logo_original.resize((130, 130))
img_logo = ImageTk.PhotoImage(img_logo_original)

l_logo = tk.Label(
    frame_esquerda,
    image=img_logo,
    width=130,
    compound="left",
    anchor="nw",
    bg=COR_PAINEL,
    fg=COR_TEXTO
)
l_logo.place(x=10, y=10)


# ==========================================
# 5. VARIÁVEIS DO PLAYER
# ==========================================

PASTA_MUSICAS = os.path.join(
    PASTA_PROJETO,
    "músicas"
)

if not os.path.isdir(PASTA_MUSICAS):
    os.makedirs(PASTA_MUSICAS)

musicas = [
    arquivo
    for arquivo in os.listdir(PASTA_MUSICAS)
    if arquivo.lower().endswith((".mp3", ".wav", ".ogg"))
]

musicas.sort()

duracao_musica = 0
posicao_atual = 0
posicao_base = 0
inicio_trecho = 0
musica_pausada = False


# ==========================================
# 6. LISTA DE MÚSICAS
# ==========================================

frame_direita.grid_rowconfigure(0, weight=1)
frame_direita.grid_columnconfigure(0, weight=1)

listbox = tk.Listbox(
    frame_direita,
    selectmode=tk.SINGLE,
    font=("Arial", 9, "bold"),
    width=22,
    bg=COR_SUPERFICIE,
    fg=COR_TEXTO,
    selectbackground=COR_ROXO,
    selectforeground=COR_FUNDO,
    relief="flat",
    borderwidth=0,
    highlightthickness=0
)

listbox.grid(
    row=0,
    column=0,
    sticky="nsew"
)

scrollbar = tk.Scrollbar(
    frame_direita,
    orient=tk.VERTICAL,
    command=listbox.yview,
    bg=COR_PAINEL,
    troughcolor=COR_SUPERFICIE,
    activebackground=COR_ROXO
)

scrollbar.grid(
    row=0,
    column=1,
    sticky="ns"
)

listbox.configure(
    yscrollcommand=scrollbar.set
)


def mostrar_musicas():
    """Insere os arquivos de áudio na lista."""
    listbox.delete(0, tk.END)

    for musica in musicas:
        listbox.insert(tk.END, musica)


mostrar_musicas()


# ==========================================
# 7. IDENTIFICAÇÃO DA MÚSICA ATUAL
# ==========================================

l_rodando = tk.Label(
    frame_baixo,
    text="Escolha a música na lista",
    width=44,
    justify=tk.LEFT,
    anchor="nw",
    font=("Arial", 9, "bold"),
    bg=COR_PAINEL,
    fg=COR_DESTAQUE
)

l_rodando.place(x=10, y=3)


# ==========================================
# 8. FUNÇÕES AUXILIARES DO PROGRESSO
# ==========================================

def formatar_tempo(segundos):
    """Converte segundos para minutos e segundos."""
    minutos = int(segundos // 60)
    segundos = int(segundos % 60)

    return f"{minutos:02d}:{segundos:02d}"


def atualizar_duracao(caminho):
    """Obtém a duração total da música."""

    global duracao_musica
    global posicao_atual
    global posicao_base
    global inicio_trecho

    arquivo = MutagenFile(caminho)

    if arquivo is not None and arquivo.info:
        duracao_musica = arquivo.info.length
    else:
        duracao_musica = 0

    posicao_atual = 0
    posicao_base = 0
    inicio_trecho = time.monotonic()

    barra_progresso.config(
        from_=0,
        to=max(duracao_musica, 1)
    )

    barra_progresso.set(0)

    tempo_atual.config(text="00:00")

    tempo_total.config(
        text=formatar_tempo(duracao_musica)
    )


def avancar_musica(event=None):
    """Permite avançar ou voltar pela barra."""

    global posicao_atual
    global posicao_base
    global inicio_trecho

    if duracao_musica <= 0:
        return

    posicao = barra_progresso.get()
    posicao = max(0, min(posicao, duracao_musica))

    try:
        mixer.music.set_pos(posicao)

        posicao_atual = posicao
        posicao_base = posicao
        inicio_trecho = time.monotonic()

        tempo_atual.config(
            text=formatar_tempo(posicao)
        )

    except pygame_error:
        messagebox.showwarning(
            "VYBE",
            "Não foi possível avançar neste formato de áudio."
        )


def atualizar_barra():
    """Atualiza automaticamente a posição da música."""

    global posicao_atual

    if not musica_pausada and mixer.music.get_busy():

        posicao_atual = (
            posicao_base +
            (time.monotonic() - inicio_trecho)
        )

        posicao_atual = min(
            posicao_atual,
            duracao_musica
        )

        barra_progresso.set(posicao_atual)

        tempo_atual.config(
            text=formatar_tempo(posicao_atual)
        )

    janela.after(500, atualizar_barra)

# ==========================================
# 9. FUNÇÕES DE REPRODUÇÃO
# ==========================================

def play_musica():
    """Reproduz a música selecionada."""

    global musica_pausada

    selecao = listbox.curselection()

    if not selecao:
        return

    indice = selecao[0]
    tocando = musicas[indice]

    caminho = os.path.join(
        PASTA_MUSICAS,
        tocando
    )

    try:
        mixer.music.load(caminho)
        mixer.music.play()

        musica_pausada = False

        atualizar_duracao(caminho)

        l_rodando.config(text=tocando)

    except Exception as erro:
        messagebox.showerror(
            "Erro ao reproduzir",
            str(erro)
        )


def pausar_musica():
    """Pausa a reprodução atual."""

    global musica_pausada
    global posicao_atual

    if mixer.music.get_busy():
        posicao_atual = (
            posicao_base +
            (time.monotonic() - inicio_trecho)
        )

        mixer.music.pause()
        musica_pausada = True


def continuar_musica():
    """Retoma a reprodução pausada."""

    global musica_pausada
    global posicao_base
    global inicio_trecho

    if musica_pausada:
        mixer.music.unpause()

        posicao_base = posicao_atual
        inicio_trecho = time.monotonic()

        musica_pausada = False


def parar_musica():
    """Interrompe a reprodução."""

    global musica_pausada
    global posicao_atual
    global posicao_base

    mixer.music.stop()

    musica_pausada = False
    posicao_atual = 0
    posicao_base = 0

    barra_progresso.set(0)

    tempo_atual.config(text="00:00")


def reproduzir_indice(indice):
    """Reproduz uma música pelo índice da lista."""

    global musica_pausada

    if not musicas:
        return

    indice = indice % len(musicas)

    tocando = musicas[indice]

    caminho = os.path.join(
        PASTA_MUSICAS,
        tocando
    )

    try:
        mixer.music.load(caminho)
        mixer.music.play()

        musica_pausada = False

        atualizar_duracao(caminho)

        listbox.selection_clear(0, tk.END)
        listbox.selection_set(indice)
        listbox.activate(indice)
        listbox.see(indice)

        l_rodando.config(text=tocando)

    except Exception as erro:
        messagebox.showerror(
            "Erro ao reproduzir",
            str(erro)
        )


def proxima_musica():
    """Avança para a próxima música."""

    if not musicas:
        return

    selecao = listbox.curselection()

    if selecao:
        indice = selecao[0]
    elif l_rodando["text"] in musicas:
        indice = musicas.index(l_rodando["text"])
    else:
        indice = -1

    reproduzir_indice(indice + 1)


def musica_anterior():
    """Volta para a música anterior."""

    if not musicas:
        return

    selecao = listbox.curselection()

    if selecao:
        indice = selecao[0]
    elif l_rodando["text"] in musicas:
        indice = musicas.index(l_rodando["text"])
    else:
        indice = 1

    reproduzir_indice(indice - 1)


# ==========================================
# 10. CARREGAMENTO DOS ÍCONES
# ==========================================

def carregar_icone(nome):
    """Carrega e redimensiona os ícones."""

    caminho = os.path.join(
        PASTA_PROJETO,
        nome
    )

    imagem = Image.open(caminho)
    imagem = imagem.resize((30, 30))

    return ImageTk.PhotoImage(imagem)


img_2 = carregar_icone("iconanterior.png")
img_3 = carregar_icone("iconplay.png")
img_4 = carregar_icone("iconproxima.png")
img_5 = carregar_icone("iconpause.png")
img_6 = carregar_icone("iconpare.png")


# ==========================================
# 11. BARRA DE PROGRESSO E TEMPOS
# ==========================================

tempo_atual = tk.Label(
    frame_baixo,
    text="00:00",
    bg=COR_PAINEL,
    fg=COR_TEXTO,
    font=("Arial", 8, "bold")
)

tempo_atual.place(x=5, y=29)

tempo_total = tk.Label(
    frame_baixo,
    text="00:00",
    bg=COR_PAINEL,
    fg=COR_TEXTO,
    font=("Arial", 8, "bold")
)

tempo_total.place(x=310, y=29)

barra_progresso = tk.Scale(
    frame_baixo,
    from_=0,
    to=1,
    orient=tk.HORIZONTAL,
    length=255,
    showvalue=False,
    resolution=0.1,
    sliderlength=12,
    width=5,
    bg=COR_PAINEL,
    fg=COR_TEXTO,
    troughcolor=COR_SUPERFICIE,
    activebackground=COR_ROXO,
    highlightthickness=0,
    bd=0
)

barra_progresso.place(x=45, y=20)

barra_progresso.bind(
    "<ButtonRelease-1>",
    avancar_musica
)

# ==========================================
# 12. CRIAÇÃO DOS BOTÕES
# ==========================================

def criar_botao(imagem, comando, posicao):
    botao = tk.Button(
        frame_baixo,
        command=comando,
        image=imagem,
        relief=tk.FLAT,
        overrelief=tk.RIDGE,
        bg=COR_SUPERFICIE,
        fg=COR_DESTAQUE,
        activebackground=COR_ROXO,
        activeforeground=COR_FUNDO,
        borderwidth=0,
        padx=5,
        pady=5
    )

    botao.place(
        relx=0.5,
        x=posicao,
        y=75,
        anchor="center"
    )

    return botao


b_anterior = criar_botao(
    img_2,
    musica_anterior,
    -140
)

b_play = criar_botao(
    img_3,
    play_musica,
    -70
)

b_proximo = criar_botao(
    img_4,
    proxima_musica,
    0
)

b_pausa = criar_botao(
    img_5,
    pausar_musica,
    70
)

b_parar = criar_botao(
    img_6,
    parar_musica,
    140
)


# ==========================================
# 13. ATUALIZAÇÃO AUTOMÁTICA
# ==========================================

janela.after(500, atualizar_barra)


# ==========================================
# 14. LOOP PRINCIPAL
# ==========================================

janela.mainloop()





