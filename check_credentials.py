#!/usr/bin/env python3
"""
Script para verificar se as credenciais estão configuradas corretamente
"""

import os
from dotenv import load_dotenv

def check_credentials():
    """Verifica se as credenciais estão configuradas"""
    load_dotenv()
    
    email = os.getenv("YOUTUBE_EMAIL")
    password = os.getenv("YOUTUBE_PASSWORD")
    
    print("🔍 Verificando configuração de credenciais...")
    print("-" * 50)
    
    if not email or email == "seu.email@gmail.com":
        print("❌ EMAIL: Não configurado ou usando valor de exemplo")
        return False
    else:
        print(f"✅ EMAIL: {email}")
    
    if not password or password == "suaSenhaSegura":
        print("❌ SENHA: Não configurada ou usando valor de exemplo")
        return False
    else:
        print(f"✅ SENHA: {'*' * len(password)} (configurada)")
    
    print("-" * 50)
    print("✅ Credenciais configuradas corretamente!")
    return True

if __name__ == "__main__":
    if check_credentials():
        print("🚀 Pronto para executar a automação!")
    else:
        print("📝 Configure suas credenciais no arquivo .env antes de continuar")
        print("   YOUTUBE_EMAIL=seu_email_real@gmail.com")
        print("   YOUTUBE_PASSWORD=sua_senha_real")
