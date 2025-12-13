#!/usr/bin/env python3
"""
Script de Teste Automatizado - Obsidian Agente v2.0
Testa todos os componentes do sistema
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5001"
API_KEY = "test_key_123"  # Será substituído pela chave real

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name, status, message=""):
    symbol = f"{Colors.GREEN}✓{Colors.END}" if status else f"{Colors.RED}✗{Colors.END}"
    print(f"{symbol} {name}")
    if message:
        print(f"  {Colors.YELLOW}{message}{Colors.END}")

def test_health():
    """Testa endpoint de health"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_test("Health Check", True, f"Status: {data.get('status')}, Version: {data.get('version')}")
            return True
        else:
            print_test("Health Check", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_test("Health Check", False, f"Erro: {str(e)}")
        return False

def test_intelligent_process():
    """Testa processamento inteligente"""
    try:
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        data = {"text": "status"}
        response = requests.post(f"{BASE_URL}/intelligent/process", json=data, headers=headers, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print_test("Intelligent Processing", result.get('success', False), 
                      f"Command: {result.get('command', 'N/A')}")
            return result.get('success', False)
        else:
            print_test("Intelligent Processing", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        print_test("Intelligent Processing", False, f"Erro: {str(e)}")
        return False

def test_knowledge_base():
    """Testa base de conhecimento"""
    try:
        # Importar módulos do agente
        sys.path.insert(0, '/home/ubuntu/obsidian-agente/agent')
        from obsidian_knowledge import ObsidianKnowledge
        
        kb = ObsidianKnowledge()
        
        # Testar conhecimento sobre wikilinks
        wikilinks_info = kb.get_feature_info('wikilinks')
        has_wikilinks = wikilinks_info is not None and len(wikilinks_info) > 0
        
        # Testar conhecimento sobre plugins
        plugins = kb.get_popular_plugins()
        has_plugins = len(plugins) > 0
        
        success = has_wikilinks and has_plugins
        print_test("Knowledge Base", success, 
                  f"Features: {len(kb.features)}, Plugins: {len(plugins)}")
        return success
    except Exception as e:
        print_test("Knowledge Base", False, f"Erro: {str(e)}")
        return False

def test_advanced_features():
    """Testa funcionalidades avançadas"""
    try:
        sys.path.insert(0, '/home/ubuntu/obsidian-agente/agent')
        from obsidian_advanced import ObsidianAdvanced
        
        adv = ObsidianAdvanced()
        
        # Testar extração de wikilinks
        test_content = "Este é um [[link]] para outra nota"
        wikilinks = adv.extract_wikilinks(test_content)
        has_wikilinks = len(wikilinks) == 1 and wikilinks[0] == "link"
        
        # Testar extração de tags
        test_content_tags = "Este é um texto com #tag1 e #tag2"
        tags = adv.extract_tags(test_content_tags)
        has_tags = len(tags) == 2
        
        success = has_wikilinks and has_tags
        print_test("Advanced Features", success, 
                  f"Wikilinks: {len(wikilinks)}, Tags: {len(tags)}")
        return success
    except Exception as e:
        print_test("Advanced Features", False, f"Erro: {str(e)}")
        return False

def main():
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}OBSIDIAN AGENTE v2.0 - TESTE AUTOMATIZADO{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    tests = [
        ("Health Check", test_health),
        ("Knowledge Base", test_knowledge_base),
        ("Advanced Features", test_advanced_features),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print_test(name, False, f"Erro inesperado: {str(e)}")
            results.append(False)
        print()
    
    # Resumo
    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100 if total > 0 else 0
    
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}RESUMO DOS TESTES{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"Total de testes: {total}")
    print(f"Testes aprovados: {Colors.GREEN}{passed}{Colors.END}")
    print(f"Testes falhados: {Colors.RED}{total - passed}{Colors.END}")
    print(f"Taxa de sucesso: {Colors.GREEN if percentage >= 80 else Colors.RED}{percentage:.1f}%{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    if percentage >= 80:
        print(f"{Colors.GREEN}✓ Sistema validado com sucesso!{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.RED}✗ Sistema apresenta problemas. Revise os erros acima.{Colors.END}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
