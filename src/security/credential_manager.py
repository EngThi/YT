"""
Credential Manager - Gestão Segura de Credenciais
=================================================

Sistema seguro para gerenciamento de credenciais com criptografia.
"""

import os
import base64
import json
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from dotenv import load_dotenv
import getpass


class CredentialManager:
    """Gerenciador seguro de credenciais"""
    
    def __init__(self, master_password: Optional[str] = None):
        self.master_password = master_password
        self.credentials_file = ".credentials.enc"
        self.salt_file = ".salt"
        self._cipher = None
        
    def _generate_key(self, password: str, salt: bytes) -> bytes:
        """Gera chave de criptografia a partir da senha mestre"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def _get_cipher(self) -> Fernet:
        """Obtém cipher para criptografia"""
        if self._cipher is None:
            if self.master_password is None:
                self.master_password = getpass.getpass("🔐 Digite a senha mestre: ")
            
            # Gera ou carrega salt
            if os.path.exists(self.salt_file):
                with open(self.salt_file, 'rb') as f:
                    salt = f.read()
            else:
                salt = os.urandom(16)
                with open(self.salt_file, 'wb') as f:
                    f.write(salt)
            
            key = self._generate_key(self.master_password, salt)
            self._cipher = Fernet(key)
        
        return self._cipher
    
    def store_credentials(self, youtube_email: str, youtube_password: str) -> bool:
        """Armazena credenciais criptografadas"""
        try:
            credentials = {
                "youtube_email": youtube_email,
                "youtube_password": youtube_password,
                "created_at": str(os.time())
            }
            
            cipher = self._get_cipher()
            encrypted_data = cipher.encrypt(json.dumps(credentials).encode())
            
            with open(self.credentials_file, 'wb') as f:
                f.write(encrypted_data)
            
            print("✅ Credenciais armazenadas com segurança")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao armazenar credenciais: {e}")
            return False
    
    def load_credentials(self) -> Optional[Dict[str, str]]:
        """Carrega credenciais descriptografadas"""
        try:
            if not os.path.exists(self.credentials_file):
                return None
            
            cipher = self._get_cipher()
            
            with open(self.credentials_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = cipher.decrypt(encrypted_data)
            credentials = json.loads(decrypted_data.decode())
            
            return {
                "email": credentials["youtube_email"],
                "password": credentials["youtube_password"]
            }
            
        except Exception as e:
            print(f"❌ Erro ao carregar credenciais: {e}")
            return None
    
    def setup_credentials_interactively(self) -> bool:
        """Configura credenciais interativamente"""
        print("🔐 CONFIGURAÇÃO SEGURA DE CREDENCIAIS")
        print("=" * 50)
        
        # Verifica se já existem credenciais
        existing_creds = self.load_credentials()
        if existing_creds:
            print("✅ Credenciais já configuradas")
            change = input("Deseja alterar as credenciais? (s/n): ").lower()
            if change != 's':
                return True
        
        # Solicita novas credenciais
        print("\n📧 Configure suas credenciais do YouTube:")
        email = input("Email: ").strip()
        
        if not email:
            print("❌ Email não pode estar vazio")
            return False
        
        password = getpass.getpass("Senha: ")
        
        if not password:
            print("❌ Senha não pode estar vazia")
            return False
        
        # Confirma senha
        password_confirm = getpass.getpass("Confirme a senha: ")
        
        if password != password_confirm:
            print("❌ Senhas não coincidem")
            return False
        
        return self.store_credentials(email, password)
    
    def get_credentials_from_env(self) -> Optional[Dict[str, str]]:
        """Tenta carregar credenciais do arquivo .env"""
        load_dotenv()
        
        email = os.getenv("YOUTUBE_EMAIL")
        password = os.getenv("YOUTUBE_PASSWORD")
        
        if email and password:
            return {"email": email, "password": password}
        
        return None
    
    def get_credentials(self) -> Optional[Dict[str, str]]:
        """Obtém credenciais por ordem de prioridade"""
        
        # 1. Tenta carregar credenciais criptografadas
        creds = self.load_credentials()
        if creds:
            return creds
        
        # 2. Tenta carregar do .env
        creds = self.get_credentials_from_env()
        if creds:
            print("⚠️  Credenciais carregadas do .env (recomenda-se usar armazenamento seguro)")
            return creds
        
        # 3. Solicita configuração interativa
        print("🔐 Nenhuma credencial encontrada. Configuração necessária:")
        if self.setup_credentials_interactively():
            return self.load_credentials()
        
        return None
    
    def remove_credentials(self) -> bool:
        """Remove credenciais armazenadas"""
        try:
            if os.path.exists(self.credentials_file):
                os.remove(self.credentials_file)
            if os.path.exists(self.salt_file):
                os.remove(self.salt_file)
            
            print("✅ Credenciais removidas com segurança")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao remover credenciais: {e}")
            return False


def create_secure_env_template():
    """Cria template .env seguro"""
    template = """# YouTube Automation - Configurações
# IMPORTANTE: NÃO COMMITAR ESTE ARQUIVO COM DADOS REAIS

# Credenciais YouTube (OPCIONAL - use credential manager para maior segurança)
YOUTUBE_EMAIL=seu.email@gmail.com
YOUTUBE_PASSWORD=suaSenhaSegura

# Configurações do Sistema
LOG_LEVEL=INFO
SCREENSHOT_ENABLED=true
HUMAN_SIMULATION=true

# Configurações Stealth
STEALTH_MODE=advanced
CONTEXT_ROTATION=true
SESSION_PERSISTENCE=true
"""
    
    with open('.env.example', 'w', encoding='utf-8') as f:
        f.write(template)
    
    print("✅ Arquivo .env.example criado")
    print("📋 Copie para .env e configure suas credenciais")
    print("🔐 Recomendação: Use o CredentialManager para maior segurança")


if __name__ == "__main__":
    # Demonstração do uso
    cm = CredentialManager()
    
    if cm.setup_credentials_interactively():
        creds = cm.get_credentials()
        if creds:
            print(f"✅ Credenciais configuradas para: {creds['email']}")
    else:
        print("❌ Falha na configuração das credenciais")
