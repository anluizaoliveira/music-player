# 🎵 VYBE | Music Player

Um player de música desenvolvido em Python, com interface gráfica construída utilizando Tkinter e uma identidade visual em tons de roxo e lavanda.

O **VYBE Music Player** foi criado com o objetivo de oferecer uma experiência simples e intuitiva para reproduzir músicas diretamente do computador.

## 🖥️ Apresentação do projeto

![Interface do VYBE](InterfaceVybe.png)

## ✨ Funcionalidades

- Listagem automática das músicas armazenadas na pasta `músicas`.
- Reprodução de arquivos de áudio.
- Controles para avançar e voltar entre as músicas.
- Opções para pausar, continuar e interromper a reprodução.
- Interface gráfica personalizada.
- Ícones personalizados para os controles do player.
- Organização das músicas em uma lista com barra de rolagem.
- Barra de progresso da reprodução.
- Suporte aos formatos MP3, WAV e OGG.

## 🛠️ Tecnologias utilizadas

O projeto foi desenvolvido utilizando:

- **Python:** linguagem de programação utilizada no desenvolvimento.
- **Tkinter:** criação da interface gráfica.
- **Pygame:** reprodução dos arquivos de áudio.
- **Pillow:** carregamento e manipulação das imagens utilizadas na interface.
- **Mutagen:** obtenção de informações sobre os arquivos de áudio.

## 📁 Estrutura do projeto

```text
music-player/
│
├── músicas/
│   ├── musica1.mp3
│   ├── musica2.mp3
│   └── ...
│
├── imagens/
│   └── tela-inicial.png
│
├── icon1.png.png
├── iconanterior.png
├── iconpare.png
├── iconpause.png
├── iconplay.png
├── iconproxima.png
│
├── vibemusic.py
└── README.md
```

## ⚙️ Instalação e execução

**1. Clone o repositório:**

```bash
git clone https://github.com/anluizaoliveira/music-player.git
```

**2. Entre na pasta do projeto:**

```bash
cd music-player
```

**3. Instale as dependências:**

```bash
python -m pip install pygame pillow mutagen
```

**4. Execute o programa:**

```bash
python vibemusic.py
```


## 🎧 Como utilizar

1. Abra o programa VYBE.
2. Adicione seus arquivos de áudio à pasta `músicas`.
3. Selecione uma música na lista.
4. Utilize os botões de controle para reproduzir, pausar, continuar, avançar ou voltar as músicas.
