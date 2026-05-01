# 🎙️ Sistema de Fila de Transcrição - Resumo das Mudanças

## O que foi implementado

Um sistema robusto de fila (queue) que permite processar **múltiplos arquivos de áudio em sequência**, com rastreamento de status, tratamento de erros e geração de logs.

---

## Arquivos Criados/Modificados

### 1. **queue_manager.py** (NOVO)
Módulo principal com duas classes:

#### `TranscriptionTask`
- Representa uma tarefa individual de transcrição
- Rastreia status: `pending`, `processing`, `completed`, `failed`
- Armazena resultado, tempo de criação/conclusão e mensagens de erro

#### `TranscriptionQueue`
Gerencia a fila com os seguintes métodos:

| Método | Função |
|--------|--------|
| `add_task()` | Adiciona um arquivo específico à fila |
| `add_tasks_from_directory()` | Adiciona todos os áudios de um diretório |
| `get_queue_status()` | Retorna estatísticas da fila |
| `process_queue()` | Processa todos os arquivos em sequência |
| `save_queue_log()` | Salva um log JSON com os resultados |
| `clear_queue()` | Limpa a fila |

### 2. **cli.py** (MODIFICADO)
Atualizações para suportar:

- ✅ **Um arquivo** (compatível com versão anterior)
- ✅ **Múltiplos arquivos** com `--audio` repetido
- ✅ **Diretório inteiro** com `--audio-dir`
- ✅ **Diferentes modelos** Whisper
- ✅ **Log opcional** com `--save-log`

---

## Como Usar

### Via Linha de Comando

#### Opção 1: Um arquivo
```bash
python -m speech_to_text.cli --audio audios/meu_audio.m4a
```

#### Opção 2: Múltiplos arquivos
```bash
python -m speech_to_text.cli \
  --audio audios/audio1.m4a \
  --audio audios/audio2.m4a \
  --audio audios/audio3.m4a
```

#### Opção 3: Diretório completo
```bash
python -m speech_to_text.cli --audio-dir audios
```

#### Opção 4: Com opções avançadas
```bash
python -m speech_to_text.cli \
  --audio-dir audios \
  --model large \
  --output-dir outputs \
  --save-log
```

### Via Python

```python
from pathlib import Path
from speech_to_text.queue_manager import TranscriptionQueue

# Criar fila
queue = TranscriptionQueue(model_name="medium")

# Adicionar arquivos
queue.add_task(Path("audios/audio1.m4a"), Path("outputs"))
queue.add_task(Path("audios/audio2.m4a"), Path("outputs"))
queue.add_task(Path("audios/audio3.m4a"), Path("outputs"))

# Processar
queue.process_queue()

# Salvar log (opcional)
queue.save_queue_log(Path("outputs/transcription_log.json"))
```

---

## Funcionalidades Principais

### 1. **Rastreamento de Status**
Cada tarefa passa por estados bem definidos:
- 🟡 **pending**: Aguardando processamento
- 🔄 **processing**: Sendo transcrita
- ✅ **completed**: Concluída com sucesso
- ❌ **failed**: Erro durante transcrição

### 2. **Processamento em Sequência**
- Processa um áudio por vez
- Não bloqueia interface (exceto durante transcrição)
- Continua mesmo com erros em arquivos individuais

### 3. **Saídas Geradas**
Para cada áudio são criados:
1. `{nome}_transcricao.txt` - Texto puro
2. `{nome}_transcricao_com_tempos.txt` - Com timestamps

### 4. **Log de Processamento** (opcional)
Arquivo `transcription_log.json` contém:
```json
{
  "timestamp": "2024-04-30T10:30:00",
  "queue_summary": {
    "total_tasks": 3,
    "pending": 0,
    "processing": 0,
    "completed": 2,
    "failed": 1
  },
  "tasks": [...]
}
```

### 5. **Relatório Final**
Exibe automaticamente:
- Total de tarefas concluídas com sucesso
- Total de falhas
- Detalhes de erros para cada falha

---

## Arquivos de Exemplo

### `examples_queue.py`
Script interativo com 4 exemplos práticos:
1. Transcrever um único áudio
2. Múltiplos áudios específicos
3. Diretório completo
4. Diferentes modelos Whisper

Execute com:
```bash
python examples_queue.py
```

### `QUEUE_USAGE.md`
Documentação completa de uso

---

## Formatos Suportados

Quando usa `--audio-dir`, detecta automaticamente:
- MP3, WAV, M4A, FLAC, OGG, WebM (maiúscula e minúscula)

---

## Compatibilidade

✅ **Totalmente compatível** com o código antigo
- Se usar um único `--audio`, funciona como antes
- Modelos, saídas e formato continuam iguais

---

## Próximos Passos (Opcional)

Possíveis melhorias futuras:
- [ ] Processamento paralelo (múltiplos áudios simultâneos)
- [ ] Interface web/GUI para gerenciar fila
- [ ] Retomada de fila interrompida
- [ ] Notificações/alertas ao concluir
- [ ] Suporte a prioridades de tarefa
