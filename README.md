# 🎙️ Audio Transcriber



\

Ferramenta em Python para **transcrição automática de áudio para texto** usando o modelo Whisper, com suporte a **FFmpeg local (sem dependência global)**.

---

## 📌 Funcionalidades

* Transcrição de áudio → texto
* Suporte a múltiplos formatos (`.mp3`, `.wav`, `.m4a`, `.ogg`)
* Geração de:

  * Texto simples
  * Texto com timestamps
* Execução via CLI
* FFmpeg isolado no projeto (portável)

---

## 🧱 Estrutura do Projeto

```text
audio-transcriber/
│
├── audios/
├── ffmpeg/
│   └── bin/
│       └── ffmpeg.exe
│
├── outputs/
│
├── src/
│   └── speech_to_text/
│       ├── __init__.py
│       ├── cli.py
│       ├── transcriber.py
│       └── utils.py
│
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🚀 Quick Start

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/audio-transcriber.git
cd audio-transcriber
```

---

### 2. Crie e ative o ambiente virtual

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração do FFmpeg (local)

Este projeto usa o FFmpeg de forma local.

### Passos:

1. Baixe o FFmpeg (build estático)
2. Extraia o conteúdo
3. Copie a pasta `bin` para:

```text
ffmpeg/bin/
```

Resultado esperado:

```text
ffmpeg/bin/ffmpeg.exe
```

---

## 🎬 Uso

```bash
python -m audio_transcriber.cli --audio "audios/seu_audio.m4a" --model medium
```

---

## ⚙️ Parâmetros

| Parâmetro      | Descrição                                                   |
| -------------- | ----------------------------------------------------------- |
| `--audio`      | Caminho do arquivo de áudio                                 |
| `--model`      | Modelo Whisper (`tiny`, `base`, `small`, `medium`, `large`) |
| `--output-dir` | Diretório de saída (default: `outputs`)                     |

---

## 📄 Saídas

### Texto simples

```text
outputs/transcricao.txt
```

### Texto com timestamps

```text
outputs/transcricao_com_tempos.txt
```

---

## 🧠 Modelos disponíveis

| Modelo | Velocidade  | Precisão   |
| ------ | ----------- | ---------- |
| tiny   | Muito alta  | Baixa      |
| base   | Alta        | Média      |
| small  | Média       | Boa        |
| medium | Baixa       | Alta       |
| large  | Muito baixa | Muito alta |

📌 Recomendação:

* `medium` → uso geral
* `large` → áudio técnico (engenharia, laboratório, etc.)

---

## ⚠️ Troubleshooting

### FFmpeg não encontrado

Verifique se existe:

```text
ffmpeg/bin/ffmpeg.exe
```

---

### Problema com imports

Execute com:

```bash
set PYTHONPATH=src
python -m audio_transcriber.cli ...
```

Ou no PowerShell:

```bash
$env:PYTHONPATH="src"
python -m audio_transcriber.cli ...
```

---

### Performance baixa

* Use modelo menor (`small`)
* Verifique uso de CPU/GPU

---

## 🛠️ Roadmap

* [ ] Diarização (múltiplos falantes)
* [ ] Interface gráfica (GUI)
* [ ] Exportação em PDF (ABNT)
* [ ] Correção automática de termos técnicos
* [ ] Empacotamento via `pip`

---

## 🤝 Contribuição

Pull requests são bem-vindos.

Para contribuir:

1. Fork do projeto
2. Crie uma branch:

```bash
git checkout -b feature/nova-feature
```

3. Commit:

```bash
git commit -m "feat: adiciona nova feature"
```

4. Push:

```bash
git push origin feature/nova-feature
```

5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT.
Veja o arquivo `LICENSE` para mais detalhes.

---

## 📚 Tecnologias

* Python
* Whisper
* FFmpeg

---

## 👨‍💻 Autor

Desenvolvido para transcrição automatizada de áudios acadêmicos e técnicos.

---


