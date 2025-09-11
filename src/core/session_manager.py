"""
Session Manager - Gerenciador de Sessões Persistentes
====================================================

Sistema avançado para gerenciamento de sessões com persistência e recuperação.
"""

import json
import time
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from cryptography.fernet import Fernet

from ..utils.logger import get_logger


@dataclass
class SessionInfo:
    """Informações de sessão"""
    session_id: str
    user_agent: str
    viewport_size: tuple
    created_at: datetime
    last_accessed: datetime
    url_history: List[str]
    login_status: str
    fingerprint_hash: str
    tags: List[str]
    metadata: Dict[str, Any]


class SessionStorage:
    """Armazenamento seguro de sessões"""
    
    def __init__(self, storage_dir: str = "sessions"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.logger = get_logger("session_storage")
        self._encryption_key = self._get_or_create_key()
    
    def _get_or_create_key(self) -> bytes:
        """Obtém ou cria chave de criptografia para sessões"""
        key_file = self.storage_dir / ".session_key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def _encrypt_data(self, data: bytes) -> bytes:
        """Criptografa dados da sessão"""
        fernet = Fernet(self._encryption_key)
        return fernet.encrypt(data)
    
    def _decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Descriptografa dados da sessão"""
        fernet = Fernet(self._encryption_key)
        return fernet.decrypt(encrypted_data)
    
    def save_session_data(self, session_id: str, cookies: List[Dict], 
                         local_storage: Dict = None, session_storage: Dict = None) -> bool:
        """Salva dados da sessão"""
        try:
            session_data = {
                "cookies": cookies,
                "local_storage": local_storage or {},
                "session_storage": session_storage or {},
                "timestamp": time.time(),
                "version": "1.0"
            }
            
            # Serializa e criptografa
            serialized = json.dumps(session_data).encode()
            encrypted = self._encrypt_data(serialized)
            
            # Salva arquivo
            session_file = self.storage_dir / f"{session_id}.session"
            with open(session_file, 'wb') as f:
                f.write(encrypted)
            
            self.logger.info(f"💾 Sessão salva: {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar sessão {session_id}: {e}")
            return False
    
    def load_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Carrega dados da sessão"""
        try:
            session_file = self.storage_dir / f"{session_id}.session"
            
            if not session_file.exists():
                return None
            
            # Carrega e descriptografa
            with open(session_file, 'rb') as f:
                encrypted = f.read()
            
            decrypted = self._decrypt_data(encrypted)
            session_data = json.loads(decrypted.decode())
            
            # Verifica idade da sessão (máximo 7 dias)
            age_hours = (time.time() - session_data["timestamp"]) / 3600
            if age_hours > 168:  # 7 dias
                self.logger.warning(f"⏰ Sessão {session_id} expirada ({age_hours:.1f}h)")
                return None
            
            self.logger.info(f"📖 Sessão carregada: {session_id}")
            return session_data
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao carregar sessão {session_id}: {e}")
            return None
    
    def delete_session(self, session_id: str) -> bool:
        """Remove sessão"""
        try:
            session_file = self.storage_dir / f"{session_id}.session"
            if session_file.exists():
                session_file.unlink()
                self.logger.info(f"🗑️  Sessão removida: {session_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"❌ Erro ao remover sessão {session_id}: {e}")
            return False
    
    def list_sessions(self) -> List[str]:
        """Lista sessões disponíveis"""
        try:
            session_files = list(self.storage_dir.glob("*.session"))
            session_ids = [f.stem for f in session_files]
            return session_ids
        except Exception as e:
            self.logger.error(f"❌ Erro ao listar sessões: {e}")
            return []
    
    def cleanup_expired_sessions(self, max_age_days: int = 7) -> int:
        """Remove sessões expiradas"""
        try:
            cutoff_time = time.time() - (max_age_days * 24 * 3600)
            removed_count = 0
            
            for session_file in self.storage_dir.glob("*.session"):
                try:
                    # Verifica timestamp do arquivo
                    if session_file.stat().st_mtime < cutoff_time:
                        session_file.unlink()
                        removed_count += 1
                except Exception:
                    continue
            
            self.logger.info(f"🧹 {removed_count} sessões expiradas removidas")
            return removed_count
            
        except Exception as e:
            self.logger.error(f"❌ Erro na limpeza de sessões: {e}")
            return 0


class SessionManager:
    """Gerenciador completo de sessões"""
    
    def __init__(self):
        self.storage = SessionStorage()
        self.logger = get_logger("session_manager")
        self.active_sessions: Dict[str, SessionInfo] = {}
        self.current_session: Optional[SessionInfo] = None
    
    def create_session(self, user_agent: str, viewport_size: tuple, 
                      fingerprint_hash: str, tags: List[str] = None) -> SessionInfo:
        """Cria nova sessão"""
        session_id = str(uuid.uuid4())
        now = datetime.now()
        
        session_info = SessionInfo(
            session_id=session_id,
            user_agent=user_agent,
            viewport_size=viewport_size,
            created_at=now,
            last_accessed=now,
            url_history=[],
            login_status="unknown",
            fingerprint_hash=fingerprint_hash,
            tags=tags or [],
            metadata={}
        )
        
        self.active_sessions[session_id] = session_info
        self.current_session = session_info
        
        self.logger.info(f"🆕 Nova sessão criada: {session_id}")
        return session_info
    
    def get_session(self, session_id: str) -> Optional[SessionInfo]:
        """Obtém informações da sessão"""
        if session_id in self.active_sessions:
            return self.active_sessions[session_id]
        
        # Tenta carregar do armazenamento
        session_data = self.storage.load_session_data(session_id)
        if session_data and "metadata" in session_data:
            try:
                # Reconstrói SessionInfo dos metadados
                meta = session_data["metadata"]
                session_info = SessionInfo(
                    session_id=session_id,
                    user_agent=meta.get("user_agent", ""),
                    viewport_size=tuple(meta.get("viewport_size", (1366, 768))),
                    created_at=datetime.fromisoformat(meta.get("created_at", datetime.now().isoformat())),
                    last_accessed=datetime.now(),
                    url_history=meta.get("url_history", []),
                    login_status=meta.get("login_status", "unknown"),
                    fingerprint_hash=meta.get("fingerprint_hash", ""),
                    tags=meta.get("tags", []),
                    metadata=meta.get("extra_metadata", {})
                )
                
                self.active_sessions[session_id] = session_info
                return session_info
                
            except Exception as e:
                self.logger.error(f"❌ Erro ao reconstruir sessão {session_id}: {e}")
        
        return None
    
    async def save_browser_session(self, browser_manager, session_info: SessionInfo) -> bool:
        """Salva estado do browser na sessão"""
        try:
            if not browser_manager.page:
                return False
            
            # Obtém cookies
            cookies = await browser_manager.page.cookies()
            
            # Obtém storage
            local_storage = await browser_manager.page.evaluate("""
                () => {
                    const storage = {};
                    for (let i = 0; i < localStorage.length; i++) {
                        const key = localStorage.key(i);
                        storage[key] = localStorage.getItem(key);
                    }
                    return storage;
                }
            """)
            
            session_storage_data = await browser_manager.page.evaluate("""
                () => {
                    const storage = {};
                    for (let i = 0; i < sessionStorage.length; i++) {
                        const key = sessionStorage.key(i);
                        storage[key] = sessionStorage.getItem(key);
                    }
                    return storage;
                }
            """)
            
            # Atualiza informações da sessão
            session_info.last_accessed = datetime.now()
            session_info.url_history.append(browser_manager.page.url)
            
            # Limita histórico a 50 URLs
            if len(session_info.url_history) > 50:
                session_info.url_history = session_info.url_history[-50:]
            
            # Prepara metadados para salvamento
            metadata = {
                "user_agent": session_info.user_agent,
                "viewport_size": list(session_info.viewport_size),
                "created_at": session_info.created_at.isoformat(),
                "last_accessed": session_info.last_accessed.isoformat(),
                "url_history": session_info.url_history,
                "login_status": session_info.login_status,
                "fingerprint_hash": session_info.fingerprint_hash,
                "tags": session_info.tags,
                "extra_metadata": session_info.metadata
            }
            
            # Salva com metadados
            success = self.storage.save_session_data(
                session_info.session_id,
                cookies,
                local_storage,
                session_storage_data
            )
            
            if success:
                # Salva metadados separadamente para facilitar carregamento
                session_data = self.storage.load_session_data(session_info.session_id)
                if session_data:
                    session_data["metadata"] = metadata
                    # Re-salva com metadados
                    serialized = json.dumps(session_data).encode()
                    encrypted = self.storage._encrypt_data(serialized)
                    session_file = self.storage.storage_dir / f"{session_info.session_id}.session"
                    with open(session_file, 'wb') as f:
                        f.write(encrypted)
            
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar sessão do browser: {e}")
            return False
    
    async def restore_browser_session(self, browser_manager, session_id: str) -> bool:
        """Restaura estado do browser da sessão"""
        try:
            session_data = self.storage.load_session_data(session_id)
            if not session_data:
                return False
            
            if not browser_manager.page:
                return False
            
            # Restaura cookies
            if "cookies" in session_data:
                await browser_manager.page.add_cookies(session_data["cookies"])
            
            # Restaura local storage
            if "local_storage" in session_data:
                for key, value in session_data["local_storage"].items():
                    await browser_manager.page.evaluate(f"""
                        localStorage.setItem('{key}', '{value}');
                    """)
            
            # Restaura session storage
            if "session_storage" in session_data:
                for key, value in session_data["session_storage"].items():
                    await browser_manager.page.evaluate(f"""
                        sessionStorage.setItem('{key}', '{value}');
                    """)
            
            # Atualiza sessão ativa
            session_info = self.get_session(session_id)
            if session_info:
                session_info.last_accessed = datetime.now()
                self.current_session = session_info
            
            self.logger.info(f"🔄 Sessão restaurada: {session_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao restaurar sessão {session_id}: {e}")
            return False
    
    def get_session_statistics(self) -> Dict[str, Any]:
        """Estatísticas das sessões"""
        all_session_ids = self.storage.list_sessions()
        active_count = len(self.active_sessions)
        
        # Análise por idade
        now = time.time()
        age_ranges = {"recent": 0, "day": 0, "week": 0, "old": 0}
        
        for session_id in all_session_ids:
            try:
                session_file = self.storage.storage_dir / f"{session_id}.session"
                age_hours = (now - session_file.stat().st_mtime) / 3600
                
                if age_hours < 1:
                    age_ranges["recent"] += 1
                elif age_hours < 24:
                    age_ranges["day"] += 1
                elif age_hours < 168:  # 1 semana
                    age_ranges["week"] += 1
                else:
                    age_ranges["old"] += 1
            except:
                continue
        
        return {
            "total_sessions": len(all_session_ids),
            "active_sessions": active_count,
            "current_session": self.current_session.session_id if self.current_session else None,
            "age_distribution": age_ranges,
            "storage_path": str(self.storage.storage_dir)
        }
    
    def update_login_status(self, session_id: str, status: str, metadata: Dict[str, Any] = None):
        """Atualiza status de login da sessão"""
        session_info = self.get_session(session_id)
        if session_info:
            session_info.login_status = status
            session_info.last_accessed = datetime.now()
            
            if metadata:
                session_info.metadata.update(metadata)
            
            self.logger.info(f"🔐 Status de login atualizado para {session_id}: {status}")


# Instância global
session_manager = SessionManager()


def get_session_manager() -> SessionManager:
    """Obtém instância do gerenciador de sessões"""
    return session_manager


if __name__ == "__main__":
    # Teste do sistema de sessões
    import asyncio
    
    async def test_sessions():
        manager = SessionManager()
        
        # Cria sessão de teste
        session = manager.create_session(
            "Mozilla/5.0 Test",
            (1920, 1080),
            "test_fingerprint",
            ["test", "demo"]
        )
        
        print(f"📋 Sessão criada: {session.session_id}")
        
        # Atualiza status
        manager.update_login_status(session.session_id, "logged_in", {"user": "test"})
        
        # Estatísticas
        stats = manager.get_session_statistics()
        print("📊 Estatísticas de Sessões:")
        print(f"Total: {stats['total_sessions']}")
        print(f"Ativas: {stats['active_sessions']}")
        print(f"Atual: {stats['current_session']}")
        
        return stats
    
    asyncio.run(test_sessions())
