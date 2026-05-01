from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

from speech_to_text.transcriber import AudioTranscriber
from speech_to_text.utils import build_output_paths


@dataclass
class TranscriptionTask:
    """Representa uma tarefa de transcrição na fila"""
    audio_path: Path
    model_name: str = "medium"
    output_dir: Optional[Path] = None
    status: str = "pending"  # pending, processing, completed, failed
    result: Optional[dict] = None
    error_message: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "audio_path": str(self.audio_path),
            "model_name": self.model_name,
            "output_dir": str(self.output_dir) if self.output_dir else None,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "error_message": self.error_message,
        }


class TranscriptionQueue:
    """Gerencia uma fila de transcrições"""

    def __init__(self, model_name: str = "medium"):
        self.queue: List[TranscriptionTask] = []
        self.model_name = model_name
        self.transcriber = AudioTranscriber(model_name=model_name)

    def add_task(
        self,
        audio_path: Path,
        output_dir: Path,
        model_name: Optional[str] = None
    ) -> None:
        """Adiciona uma tarefa à fila"""
        if not audio_path.exists():
            raise FileNotFoundError(f"Áudio não encontrado: {audio_path}")

        task = TranscriptionTask(
            audio_path=audio_path,
            model_name=model_name or self.model_name,
            output_dir=output_dir,
        )
        self.queue.append(task)
        print(f"✓ Tarefa adicionada: {audio_path.name}")

    def add_tasks_from_directory(
        self,
        directory: Path,
        output_dir: Path,
        extensions: List[str] = None,
    ) -> None:
        """Adiciona todas as áudios de um diretório à fila"""
        if extensions is None:
            extensions = [".mp3", ".wav", ".m4a", ".flac", ".ogg", ".webm"]

        audio_files = []
        for ext in extensions:
            audio_files.extend(directory.glob(f"*{ext}"))
            audio_files.extend(directory.glob(f"*{ext.upper()}"))

        if not audio_files:
            print(f"⚠ Nenhum arquivo de áudio encontrado em: {directory}")
            return

        for audio_path in sorted(set(audio_files)):
            try:
                self.add_task(audio_path, output_dir)
            except FileNotFoundError as e:
                print(f"✗ Erro ao adicionar {audio_path.name}: {e}")

    def get_queue_status(self) -> dict:
        """Retorna o status da fila"""
        total = len(self.queue)
        pending = sum(1 for t in self.queue if t.status == "pending")
        processing = sum(1 for t in self.queue if t.status == "processing")
        completed = sum(1 for t in self.queue if t.status == "completed")
        failed = sum(1 for t in self.queue if t.status == "failed")

        return {
            "total_tasks": total,
            "pending": pending,
            "processing": processing,
            "completed": completed,
            "failed": failed,
        }

    def process_queue(self, verbose: bool = True) -> None:
        """Processa todas as tarefas na fila"""
        if not self.queue:
            print("A fila está vazia.")
            return

        status = self.get_queue_status()
        print(f"\n{'='*60}")
        print(f"INICIANDO PROCESSAMENTO DE FILA")
        print(f"Total de tarefas: {status['total_tasks']}")
        print(f"{'='*60}\n")

        for index, task in enumerate(self.queue, 1):
            if task.status != "pending":
                continue

            print(f"[{index}/{status['total_tasks']}] Processando: {task.audio_path.name}")
            print(f"Modelo: {task.model_name}")

            try:
                task.status = "processing"

                # Transcrever áudio
                result = self.transcriber.transcribe(task.audio_path)
                task.result = result

                # Salvar resultados
                plain_output_path, timestamps_output_path = build_output_paths(
                    audio_path=task.audio_path,
                    output_dir=task.output_dir,
                )

                self.transcriber.save_plain_text(result, plain_output_path)
                self.transcriber.save_with_timestamps(result, timestamps_output_path)

                task.status = "completed"
                task.completed_at = datetime.now().isoformat()

                print(f"✓ Concluído: {plain_output_path.name}")
                print(f"✓ Concluído: {timestamps_output_path.name}\n")

            except Exception as e:
                task.status = "failed"
                task.error_message = str(e)
                task.completed_at = datetime.now().isoformat()
                print(f"✗ Erro na transcrição: {e}\n")

        self._print_summary()

    def _print_summary(self) -> None:
        """Imprime um resumo do processamento"""
        status = self.get_queue_status()

        print(f"{'='*60}")
        print(f"RESUMO DO PROCESSAMENTO")
        print(f"{'='*60}")
        print(f"Concluídas com sucesso: {status['completed']}")
        print(f"Falhadas: {status['failed']}")
        print(f"Total processadas: {status['completed'] + status['failed']}")
        print(f"{'='*60}\n")

        if status["failed"] > 0:
            print("Tarefas que falharam:")
            for task in self.queue:
                if task.status == "failed":
                    print(f"  • {task.audio_path.name}: {task.error_message}")

    def save_queue_log(self, log_path: Path) -> None:
        """Salva um log da fila em JSON"""
        log_path.parent.mkdir(parents=True, exist_ok=True)

        log_data = {
            "timestamp": datetime.now().isoformat(),
            "queue_summary": self.get_queue_status(),
            "tasks": [task.to_dict() for task in self.queue],
        }

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)

        print(f"Log salvo em: {log_path}")

    def clear_queue(self) -> None:
        """Limpa a fila"""
        self.queue.clear()
