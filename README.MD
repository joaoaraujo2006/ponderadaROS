# Atividade ROS — Turtlesim Desenhista

Projeto da disciplina de **Robótica** do Módulo 6 — Engenharia de Computação (Inteli).

O objetivo é desenvolver, do zero, um algoritmo de visão computacional capaz de **ler uma imagem, extrair seu contorno** e, em seguida, usar um pacote **ROS 2** para fazer a tartaruga do `turtlesim` **percorrer e desenhar esse contorno** na tela.

## Informações do Aluno

- **Nome:** João Pedro Gonçalves Corrêa Araujo
- **Turma:** Eng. Comp. — T16

## Estrutura do Projeto

```
Ponderada ROS/
├── PonderadaROS.ipynb        # Notebook com todo o pipeline de visão computacional
├── caminho_tartaruga.txt     # Coordenadas do contorno geradas pelo notebook
├── zara.png                  # Imagem de entrada usada para extrair o contorno
├── dog.png                   # Imagem alternativa para testes
├── requirements.txt          # Dependências Python do notebook
├── assets/                   # Imagens auxiliares (Sobel etc.)
└── tartaruga/                # Pacote ROS 2 que controla o turtlesim
    ├── package.xml
    ├── setup.py
    ├── setup.cfg
    └── tartaruga/
        └── __init__.py       # Nó controlador (entry point "controlador")
```

## Pipeline

O fluxo completo está documentado no notebook [PonderadaROS.ipynb](PonderadaROS.ipynb) e é dividido em cinco etapas:

1. **Pré-processamento** — conversão manual da imagem para escala de cinza usando os pesos perceptivos do olho humano (R: 0.299, G: 0.587, B: 0.114).
2. **Detecção de bordas** — binarização da imagem e aplicação manual do operador de **Sobel** (convolução 3x3) nos eixos X e Y, com posterior combinação por magnitude.
3. **Planejamento de caminho** — mapeamento dos pixels de borda para o espaço do turtlesim (0 a 11) e ordenação dos pontos pelo algoritmo do **vizinho mais próximo**, garantindo um traçado contínuo.
4. **Controle ROS 2** — nó em Python que lê o arquivo `caminho_tartaruga.txt` e guia a tartaruga ponto a ponto, controlando velocidade linear e angular.
5. **Vídeo de demonstração** — registro do resultado final.


## Instalação

### 1. Dependências do notebook (visão computacional)

```bash
python -m venv venv
source venv/bin/activate    # Linux/WSL
# venv\Scripts\activate     # Windows PowerShell
pip install -r requirements.txt
```

### 2. Build do pacote ROS 2

```bash
cd tartaruga
colcon build
source install/setup.bash
```

## Como Executar

### 1. Gerar o arquivo de caminho

Abra e execute o notebook [PonderadaROS.ipynb](PonderadaROS.ipynb) até a etapa de planejamento de caminho. Isso gera o arquivo `caminho_tartaruga.txt`.

> **Atenção:** o caminho do arquivo está fixado em [tartaruga/tartaruga/\_\_init\_\_.py](tartaruga/tartaruga/__init__.py#L8). Ajuste a constante `ARQUIVO` para o caminho correto no seu ambiente antes de rodar o nó.

### 2. Iniciar o turtlesim

Em um terminal com o ROS 2 ativo:

```bash
ros2 run turtlesim turtlesim_node
```

### 3. Executar o controlador

Em outro terminal:

```bash
source install/setup.bash
ros2 run tartaruga controlador
```

A tartaruga começará a percorrer o contorno extraído da imagem, desenhando-o na tela do `turtlesim`.

## Tópicos e Serviços ROS Utilizados

| Recurso | Tipo | Descrição |
|---|---|---|
| `/turtle1/cmd_vel` | `geometry_msgs/Twist` | Publica comandos de velocidade |
| `/turtle1/pose` | `turtlesim/Pose` | Assina a posição atual da tartaruga |
| `/turtle1/set_pen` | `turtlesim/SetPen` | Configura a cor e largura da caneta |

## Demonstração

O vídeo abaixo mostra a tartaruga do `turtlesim` percorrendo o contorno extraído da imagem de entrada:

[![Vídeo de demonstração](https://img.youtube.com/vi/B_S2ougmi9M/0.jpg)](https://youtu.be/B_S2ougmi9M)


