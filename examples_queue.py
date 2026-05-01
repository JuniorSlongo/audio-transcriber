#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de exemplo para usar o sistema de fila de transcrição.
Execute este arquivo para testar a fila com múltiplos áudios.
"""

from pathlib import Path
from speech_to_text.queue_manager import TranscriptionQueue
from speech_to_text.utils import get_project_root


def example_1_single_audio():
    """Exemplo 1: Transcrever um único áudio"""
    print("\n" + "="*60)
    print("EXEMPLO 1: Transcrever um único áudio")
    print("="*60)
    
    project_root = get_project_root()
    audio_file = project_root / "audios" / "seu_audio.m4a"
    output_dir = project_root / "outputs"
    
    queue = TranscriptionQueue(model_name="medium")
    
    try:
        queue.add_task(audio_file, output_dir)
        queue.process_queue()
    except FileNotFoundError as e:
        print(f"Erro: {e}")


def example_2_multiple_audios():
    """Exemplo 2: Transcrever múltiplos áudios específicos"""
    print("\n" + "="*60)
    print("EXEMPLO 2: Transcrever múltiplos áudios específicos")
    print("="*60)
    
    project_root = get_project_root()
    output_dir = project_root / "outputs"
    
    queue = TranscriptionQueue(model_name="medium")
    
    # Adicionar múltiplos arquivos
    audio_files = [
        "audios/audio1.m4a",
        "audios/audio2.m4a",
        "audios/audio3.m4a",
    ]
    
    for audio_file in audio_files:
        try:
            audio_path = project_root / audio_file
            queue.add_task(audio_path, output_dir)
        except FileNotFoundError as e:
            print(f"Erro ao adicionar {audio_file}: {e}")
    
    # Processar todos de uma vez
    queue.process_queue()


def example_3_directory():
    """Exemplo 3: Transcrever todos os áudios de um diretório"""
    print("\n" + "="*60)
    print("EXEMPLO 3: Transcrever todos os áudios de um diretório")
    print("="*60)
    
    project_root = get_project_root()
    audio_dir = project_root / "audios"
    output_dir = project_root / "outputs"
    
    queue = TranscriptionQueue(model_name="base")  # base é mais rápido
    
    # Adicionar todos os arquivos do diretório
    queue.add_tasks_from_directory(audio_dir, output_dir)
    
    # Processar
    queue.process_queue()
    
    # Salvar log
    queue.save_queue_log(output_dir / "transcription_log.json")


def example_4_different_models():
    """Exemplo 4: Transcrever com diferentes modelos"""
    print("\n" + "="*60)
    print("EXEMPLO 4: Transcrever com diferentes modelos")
    print("="*60)
    
    project_root = get_project_root()
    output_dir = project_root / "outputs"
    
    # Usar modelo pequeno para teste rápido
    queue = TranscriptionQueue(model_name="tiny")
    
    try:
        audio1 = project_root / "audios" / "audio1.m4a"
        audio2 = project_root / "audios" / "audio2.m4a"
        
        queue.add_task(audio1, output_dir, model_name="tiny")
        queue.add_task(audio2, output_dir, model_name="small")
        
        queue.process_queue()
    except FileNotFoundError as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    print("\n🎙️  Sistema de Fila de Transcrição de Áudios")
    print("Escolha um exemplo para executar:")
    print("1. Transcrever um único áudio")
    print("2. Transcrever múltiplos áudios específicos")
    print("3. Transcrever todos os áudios de um diretório")
    print("4. Transcrever com diferentes modelos")
    
    choice = input("\nDigite o número do exemplo (1-4): ").strip()
    
    examples = {
        "1": example_1_single_audio,
        "2": example_2_multiple_audios,
        "3": example_3_directory,
        "4": example_4_different_models,
    }
    
    if choice in examples:
        examples[choice]()
    else:
        print("Opção inválida!")
