#!/usr/bin/env python3
"""Script de teste para a integração Ollama no Obsidian Agent"""

import sys
sys.path.insert(0, r'C:\Users\rudpa\obsidian-agente\agent')

from ollama_integration import OllamaIntegration, AIRouter, get_ai_router

def main():
    print("=" * 60)
    print("TESTE DE INTEGRAÇÃO OLLAMA - OBSIDIAN AGENT v5.0")
    print("=" * 60)
    
    # Inicializar roteador
    router = get_ai_router()
    
    print(f"\n[INFO] Ollama disponível: {router.ollama.is_available}")
    print(f"[INFO] Modelos instalados: {router.ollama.available_models}")
    print(f"[INFO] Modelo padrão: {router.ollama.default_model}")
    
    # Testes de roteamento
    print("\n" + "-" * 60)
    print("TESTES DE ROTEAMENTO")
    print("-" * 60)
    
    testes = [
        ("Manus: pesquise sobre Angular", "manus"),
        ("Llama: o que é Python?", "ollama"),
        ("Local: traduza hello world", "ollama"),
        ("explique machine learning", "ollama"),
        ("pesquise na internet sobre IA", "manus"),
        ("abra o navegador", "manus"),
        ("crie uma nota no obsidian", "manus"),
        ("calcule 2 + 2", "ollama"),
        ("instale o nodejs", "manus"),
        ("resuma este texto", "ollama"),
    ]
    
    for mensagem, esperado in testes:
        resultado = router.route(mensagem)
        status = "OK" if resultado["provider"] == esperado else "FALHA"
        print(f"[{status}] '{mensagem[:40]}...' -> {resultado['provider']} (esperado: {esperado})")
    
    # Teste de geração real se Ollama disponível
    if router.ollama.is_available:
        print("\n" + "-" * 60)
        print("TESTE DE GERAÇÃO REAL (OLLAMA)")
        print("-" * 60)
        
        resposta = router.ollama.generate("Diga 'Olá, integração funcionando!' em uma linha.")
        print(f"Resposta Ollama: {resposta[:200]}...")
    
    print("\n" + "=" * 60)
    print("TESTE CONCLUÍDO")
    print("=" * 60)

if __name__ == "__main__":
    main()

