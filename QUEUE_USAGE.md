# Sistema de Fila de Transcrição de Áudios

Este sistema permite transcrever múltiplos arquivos de áudio em fila usando o Whisper.

## Como Usar

### 1. Transcrever um único arquivo (compatível com versão anterior)
```bash
python -m speech_to_text.cli --audio audios/meu_audio.m4a
```

### 2. Transcrever múltiplos arquivos específicos
```bash
python -m speech_to_text.cli --audio audios/audio1.m4a --audio audios/audio2.m4a --audio audios/audio3.m4a
```

### 3. Transcrever todos os áudios de um diretório
```bash
python -m speech_to_text.cli --audio-dir audios
```

### 4. Com opções avançadas
```bash
python -m speech_to_text.cli \
  --audio-dir audios \
  --model large \
  --output-dir custom_outputs \
  --save-log
```

## Opções Disponíveis

- `--audio`: Caminho de um arquivo de áudio (pode ser repetido)
- `--audio-dir`: Caminho de um diretório com múltiplos áudios
- `--model`: Modelo Whisper (tiny, base, small, medium, large) - padrão: medium
- `--output-dir`: Diretório de saída - padrão: outputs
- `--save-log`: Salva um log JSON (transcription_log.json) após o processamento

## Formatos de Áudio Suportados

- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- FLAC (.flac)
- OGG (.ogg)
- WebM (.webm)

## Exemplo de Uso em Python

```python
from pathlib import Path
from speech_to_text.queue_manager import TranscriptionQueue

# Criar fila
queue = TranscriptionQueue(model_name="medium")

# Adicionar arquivos
queue.add_task(Path("audios/audio1.m4a"), Path("outputs"))
queue.add_task(Path("audios/audio2.m4a"), Path("outputs"))

# Processar todos os arquivos
queue.process_queue()

# Salvar log
queue.save_queue_log(Path("outputs/transcription_log.json"))
```

## Saídas

Para cada arquivo de áudio, são gerados dois arquivos:
- `{audio_name}_transcricao.txt`: Transcrição em texto puro
- `{audio_name}_transcricao_com_tempos.txt`: Transcrição com timestamps (HH:MM:SS)

## Log de Processamento

Se usar `--save-log`, um arquivo `transcription_log.json` será criado com informações sobre:
- Status de cada tarefa
- Erros encontrados
- Tempo de criação e conclusão
