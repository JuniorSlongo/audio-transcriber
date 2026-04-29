# Audio Transcriber

Ferramenta em Python para transcricao automatica de audio em portugues usando Whisper, com FFmpeg local dentro do proprio projeto.

## Visao Geral

Este projeto faz:

- Leitura de arquivos de audio.
- Transcricao para texto corrido.
- Geracao de arquivo com timestamps por segmento.

Arquivos de saida gerados por padrao:

- `outputs/transcricao.txt`
- `outputs/transcricao_com_tempos.txt`

## Como Funciona

O fluxo da CLI e:

1. Valida os argumentos (`--audio`, `--model`, `--output-dir`).
2. Resolve a raiz do projeto automaticamente.
3. Adiciona `ffmpeg/bin` ao `PATH` em tempo de execucao.
4. Carrega o modelo Whisper escolhido.
5. Transcreve o audio com `language="pt"` (portugues fixo).
6. Salva dois arquivos de saida no diretorio definido.

Observacoes importantes:

- A linguagem esta fixa em portugues no codigo atual.
- O Whisper imprime logs detalhados (`verbose=True`).
- Na primeira execucao de cada modelo, o download pode demorar.

## Estrutura do Projeto

```text
audioTranscriptor/
├── audios/
├── ffmpeg/
│   └── bin/
├── outputs/
├── src/
│   └── speech_to_text/
│       ├── __init__.py
│       ├── cli.py
│       ├── transcriber.py
│       └── utils.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.9+ (recomendado 3.10 ou superior).
- FFmpeg local em `ffmpeg/bin`.
- Dependencias Python instaladas via `requirements.txt`.

## Instalacao Passo a Passo

### 1. Criar ambiente virtual

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar FFmpeg local

Coloque os executaveis do FFmpeg na pasta:

```text
ffmpeg/bin/
```

No Windows, o esperado e existir:

```text
ffmpeg/bin/ffmpeg.exe
```

O projeto nao depende de FFmpeg instalado globalmente no sistema.

## Executando a CLI

O jeito mais pratico (sem usar `PYTHONPATH`) e instalar o projeto em modo editavel uma vez:

```bash
pip install -e .
```

Depois disso, voce pode executar direto com o comando:

```bash
audio-transcriber --audio "audios/meu_audio.m4a" --model medium
```

Opcao alternativa (sem instalar em modo editavel):

Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m speech_to_text.cli --audio "audios/meu_audio.m4a" --model medium
```

Linux/macOS:

```bash
PYTHONPATH=src python -m speech_to_text.cli --audio "audios/meu_audio.m4a" --model medium
```

## Argumentos da Linha de Comando

### `--audio` (obrigatorio)

Caminho do arquivo de audio.

Exemplos:

```bash
--audio "audios/aula_01.m4a"
--audio "audios/reuniao.mp3"
--audio "C:/Users/voce/Desktop/audio.wav"
```

Notas:

- Aceita caminho relativo ao projeto ou absoluto.
- Se o arquivo nao existir, a execucao falha com `FileNotFoundError`.

### `--model` (opcional, padrao: `medium`)

Valores permitidos:

- `tiny`
- `base`
- `small`
- `medium`
- `large`

Comparacao pratica:

| Modelo | Velocidade | Precisao |
| --- | --- | --- |
| tiny | Muito alta | Mais baixa |
| base | Alta | Basica |
| small | Media | Boa |
| medium | Menor | Alta |
| large | Baixa | Muito alta |

Recomendacao inicial:

- Uso geral: `medium`
- Maquina simples/rapidez: `small`
- Maxima qualidade: `large`

### `--output-dir` (opcional, padrao: `outputs`)

Define onde os arquivos gerados serao salvos.

Exemplo:

```bash
audio-transcriber --audio "audios/aula.m4a" --output-dir "outputs/aula_01"
```

Saidas esperadas nesse caso:

- `outputs/aula_01/transcricao.txt`
- `outputs/aula_01/transcricao_com_tempos.txt`

## Exemplos Completos

### Exemplo 1: transcricao padrao

```bash
audio-transcriber --audio "audios/entrevista.m4a"
```

Resultado:

- Usa modelo `medium`.
- Gera arquivos em `outputs/`.

### Exemplo 2: modelo rapido + pasta dedicada

```bash
audio-transcriber --audio "audios/reuniao.mp3" --model small --output-dir "outputs/reuniao_2026_04_29"
```

Resultado:

- Menos tempo de execucao comparado ao `medium`.
- Arquivos separados por execucao.

## Formato dos Arquivos de Saida

### `transcricao.txt`

Contem apenas o texto final consolidado.

Exemplo:

```text
Bom dia, vamos iniciar a reuniao de planejamento do projeto...
```

### `transcricao_com_tempos.txt`

Contem cada segmento com inicio e fim no formato `HH:MM:SS`.

Exemplo:

```text
[00:00:00 - 00:00:04] Bom dia, vamos iniciar a reuniao.
[00:00:04 - 00:00:09] Hoje vamos alinhar as entregas da sprint.
```

## Erros Comuns e Solucoes

### 1. `FFmpeg local nao encontrado`

Causa:

- Pasta `ffmpeg/bin` nao existe ou esta vazia.

Como resolver:

1. Verifique a estrutura `ffmpeg/bin`.
2. Confirme que o executavel do FFmpeg esta dentro dessa pasta.

### 2. `No module named 'speech_to_text'`

Causa:

- Python nao esta encontrando a pasta `src`.

Como resolver:

1. Rode `pip install -e .` (recomendado).
2. Se preferir nao instalar, defina `PYTHONPATH=src` antes de executar.

### 3. `Audio nao encontrado`

Causa:

- Caminho informado em `--audio` esta incorreto.

Como resolver:

1. Confirme nome e extensao do arquivo.
2. Evite erros de espacos e acentuacao no caminho.
3. Teste com caminho absoluto para validar.

### 4. Execucao lenta

Causa:

- Modelo grande em maquina sem aceleracao adequada.

Como resolver:

1. Troque para `small` ou `base`.
2. Feche outros processos pesados durante a transcricao.

## Boas Praticas de Uso

- Mantenha os audios organizados em subpastas por data ou projeto.
- Use `--output-dir` diferente por execucao para nao sobrescrever arquivos.
- Se precisar de mais contexto temporal, priorize `transcricao_com_tempos.txt`.
- Comece com `small` para teste rapido e depois rode com `medium` para versao final.

## Limites Atuais

- Idioma fixo em portugues no codigo atual.
- Ainda nao ha diarizacao (separacao por falante).
- Ainda nao ha interface grafica.

## Proximos Passos Sugeridos (Roadmap)

- Parametro de idioma via CLI (`--language`).
- Parametro para ligar/desligar `verbose`.
- Nome de arquivo de saida customizavel.
- Exportacao para formatos adicionais (SRT, VTT, JSON).

## Licenca

Defina aqui a licenca do projeto (ex.: MIT) quando o arquivo de licenca estiver incluido no repositorio.


