#!/usr/bin/env python3
"""
Script de instalação e configuração do Robô IQ Option
"""

import os
import sys
import subprocess
import shutil

def print_banner():
    """Imprime banner do robô"""
    print("=" * 60)
    print("🤖 INSTALADOR DO ROBÔ IQ OPTION")
    print("=" * 60)
    print("Este script irá configurar o robô de trading automaticamente")
    print("=" * 60)

def check_python_version():
    """Verifica versão do Python"""
    print("🐍 Verificando versão do Python...")
    
    if sys.version_info < (3, 7):
        print("❌ ERRO: Python 3.7 ou superior é necessário!")
        print(f"Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def install_dependencies():
    """Instala dependências"""
    print("\n📦 Instalando dependências...")
    
    try:
        # Atualiza pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Instala dependências
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ Dependências instaladas com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def setup_environment():
    """Configura arquivo de ambiente"""
    print("\n⚙️  Configurando arquivo de ambiente...")
    
    env_file = ".env"
    env_example = ".env.example"
    
    if os.path.exists(env_file):
        print("⚠️  Arquivo .env já existe!")
        overwrite = input("Deseja sobrescrever? (s/N): ").lower()
        if overwrite != 's':
            print("📝 Mantendo arquivo .env existente")
            return True
    
    if os.path.exists(env_example):
        shutil.copy(env_example, env_file)
        print("✅ Arquivo .env criado!")
        print("📝 IMPORTANTE: Edite o arquivo .env com suas credenciais da IQ Option")
        return True
    else:
        print("❌ Arquivo .env.example não encontrado!")
        return False

def create_directories():
    """Cria diretórios necessários"""
    print("\n📁 Criando diretórios...")
    
    directories = ['logs', 'data']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Diretório '{directory}' criado")
        else:
            print(f"📁 Diretório '{directory}' já existe")

def run_tests():
    """Executa testes"""
    print("\n🧪 Executando testes...")
    
    try:
        result = subprocess.run([sys.executable, "test_bot.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Testes passaram!")
            return True
        else:
            print("⚠️  Alguns testes falharam, mas o robô pode funcionar")
            print("Saída dos testes:")
            print(result.stdout)
            return True
            
    except FileNotFoundError:
        print("⚠️  Arquivo de testes não encontrado")
        return True

def show_next_steps():
    """Mostra próximos passos"""
    print("\n" + "=" * 60)
    print("🎉 INSTALAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Edite o arquivo .env com suas credenciais da IQ Option")
    print("2. Configure o arquivo config.py conforme suas preferências")
    print("3. Teste o robô em modo backtest:")
    print("   python main.py --mode backtest")
    print("4. Execute o robô em modo live:")
    print("   python main.py --mode live")
    print("\n⚠️  AVISOS IMPORTANTES:")
    print("- Sempre teste primeiro em modo backtest")
    print("- Comece com valores pequenos")
    print("- Monitore o robô durante a execução")
    print("- Trading envolve risco de perda de capital")
    print("\n📚 Para mais informações, consulte o README.md")
    print("=" * 60)

def main():
    """Função principal"""
    print_banner()
    
    # Verifica Python
    if not check_python_version():
        sys.exit(1)
    
    # Instala dependências
    if not install_dependencies():
        print("❌ Falha na instalação das dependências")
        sys.exit(1)
    
    # Configura ambiente
    if not setup_environment():
        print("❌ Falha na configuração do ambiente")
        sys.exit(1)
    
    # Cria diretórios
    create_directories()
    
    # Executa testes
    run_tests()
    
    # Mostra próximos passos
    show_next_steps()

if __name__ == "__main__":
    main()