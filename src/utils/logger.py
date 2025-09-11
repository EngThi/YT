"""
Logger - Sistema de Logs Estruturado
====================================

Sistema avançado de logging com múltiplos níveis e formatação estruturada.
"""

import logging
import logging.handlers
import json
import os
import sys
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from enum import Enum


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class ColoredFormatter(logging.Formatter):
    """Formatter com cores para console"""
    
    # Cores ANSI
    COLORS = {
        'DEBUG': '\033[36m',      # Ciano
        'INFO': '\033[32m',       # Verde
        'WARNING': '\033[33m',    # Amarelo
        'ERROR': '\033[31m',      # Vermelho
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset_color = self.COLORS['RESET']
        
        # Adiciona cor ao nome do nível
        record.levelname = f"{log_color}{record.levelname}{reset_color}"
        
        return super().format(record)


class StructuredFormatter(logging.Formatter):
    """Formatter para logs estruturados (JSON)"""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Adiciona informações extras se disponíveis
        if hasattr(record, 'extra_data'):
            log_entry['data'] = record.extra_data
        
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry, ensure_ascii=False)


class AutomationLogger:
    """Logger personalizado para automação"""
    
    def __init__(self, name: str = "yt_automation", 
                 log_level: LogLevel = LogLevel.INFO,
                 log_dir: str = "logs",
                 max_bytes: int = 10485760,  # 10MB
                 backup_count: int = 5):
        
        self.name = name
        self.log_level = log_level
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Cria logger principal
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level.value)
        
        # Remove handlers existentes para evitar duplicação
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Configura handlers
        self._setup_console_handler()
        self._setup_file_handler(max_bytes, backup_count)
        self._setup_error_file_handler(max_bytes, backup_count)
        
        # Evita propagação para root logger
        self.logger.propagate = False
    
    def _setup_console_handler(self):
        """Configura handler para console com cores"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level.value)
        
        console_format = ColoredFormatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
    
    def _setup_file_handler(self, max_bytes: int, backup_count: int):
        """Configura handler para arquivo principal"""
        log_file = self.log_dir / f"{self.name}.log"
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)  # Arquivo mantém todos os logs
        
        file_format = StructuredFormatter()
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)
    
    def _setup_error_file_handler(self, max_bytes: int, backup_count: int):
        """Configura handler separado para erros"""
        error_file = self.log_dir / f"{self.name}_errors.log"
        
        error_handler = logging.handlers.RotatingFileHandler(
            error_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        
        error_format = StructuredFormatter()
        error_handler.setFormatter(error_format)
        self.logger.addHandler(error_handler)
    
    def debug(self, message: str, extra_data: Dict[str, Any] = None):
        """Log de debug"""
        self._log(logging.DEBUG, message, extra_data)
    
    def info(self, message: str, extra_data: Dict[str, Any] = None):
        """Log de informação"""
        self._log(logging.INFO, message, extra_data)
    
    def warning(self, message: str, extra_data: Dict[str, Any] = None):
        """Log de aviso"""
        self._log(logging.WARNING, message, extra_data)
    
    def error(self, message: str, extra_data: Dict[str, Any] = None, exc_info: bool = False):
        """Log de erro"""
        self._log(logging.ERROR, message, extra_data, exc_info)
    
    def critical(self, message: str, extra_data: Dict[str, Any] = None, exc_info: bool = False):
        """Log crítico"""
        self._log(logging.CRITICAL, message, extra_data, exc_info)
    
    def _log(self, level: int, message: str, extra_data: Dict[str, Any] = None, exc_info: bool = False):
        """Método interno para logging"""
        extra = {}
        if extra_data:
            extra['extra_data'] = extra_data
        
        self.logger.log(level, message, extra=extra, exc_info=exc_info)
    
    # Métodos específicos para automação
    def automation_start(self, action: str, target: str = None):
        """Log de início de ação de automação"""
        data = {"action": action, "status": "started"}
        if target:
            data["target"] = target
        
        self.info(f"🚀 Iniciando: {action}", data)
    
    def automation_success(self, action: str, duration: float = None, result: Any = None):
        """Log de sucesso de automação"""
        data = {"action": action, "status": "success"}
        if duration:
            data["duration_seconds"] = duration
        if result:
            data["result"] = str(result)
        
        self.info(f"✅ Sucesso: {action}", data)
    
    def automation_failure(self, action: str, error: str, duration: float = None):
        """Log de falha de automação"""
        data = {
            "action": action,
            "status": "failed",
            "error": error
        }
        if duration:
            data["duration_seconds"] = duration
        
        self.error(f"❌ Falha: {action}", data)
    
    def browser_event(self, event_type: str, url: str = None, details: Dict[str, Any] = None):
        """Log de eventos do browser"""
        data = {"event_type": event_type}
        if url:
            data["url"] = url
        if details:
            data.update(details)
        
        self.info(f"🌐 Browser: {event_type}", data)
    
    def security_event(self, event_type: str, details: Dict[str, Any] = None):
        """Log de eventos de segurança"""
        data = {"security_event": event_type}
        if details:
            data.update(details)
        
        self.warning(f"🛡️  Segurança: {event_type}", data)
    
    def performance_metric(self, metric_name: str, value: float, unit: str = "ms"):
        """Log de métricas de performance"""
        data = {
            "metric": metric_name,
            "value": value,
            "unit": unit,
            "timestamp": datetime.now().isoformat()
        }
        
        self.info(f"📊 Métrica: {metric_name}={value}{unit}", data)
    
    def user_interaction(self, interaction_type: str, element: str = None, details: Dict[str, Any] = None):
        """Log de interações do usuário simulado"""
        data = {"interaction": interaction_type}
        if element:
            data["element"] = element
        if details:
            data.update(details)
        
        self.debug(f"👤 Interação: {interaction_type}", data)


class LogManager:
    """Gerenciador global de logs"""
    
    _instance = None
    _loggers: Dict[str, AutomationLogger] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_logger(cls, name: str = "yt_automation", 
                   log_level: LogLevel = LogLevel.INFO) -> AutomationLogger:
        """Obtém ou cria logger"""
        
        if name not in cls._loggers:
            cls._loggers[name] = AutomationLogger(name, log_level)
        
        return cls._loggers[name]
    
    @classmethod
    def set_global_level(cls, level: LogLevel):
        """Define nível global de logging"""
        for logger in cls._loggers.values():
            logger.logger.setLevel(level.value)
    
    @classmethod
    def shutdown_all(cls):
        """Encerra todos os loggers"""
        for logger in cls._loggers.values():
            for handler in logger.logger.handlers:
                handler.close()
        
        cls._loggers.clear()


# Instância global para facilitar uso
default_logger = LogManager.get_logger()


# Funções de conveniência
def get_logger(name: str = "yt_automation") -> AutomationLogger:
    """Função de conveniência para obter logger"""
    return LogManager.get_logger(name)


def log_execution_time(func):
    """Decorator para logar tempo de execução"""
    import functools
    import time
    
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        logger = get_logger()
        
        try:
            logger.automation_start(func.__name__)
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.automation_success(func.__name__, duration, result)
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.automation_failure(func.__name__, str(e), duration)
            raise
    
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        logger = get_logger()
        
        try:
            logger.automation_start(func.__name__)
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.automation_success(func.__name__, duration, result)
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.automation_failure(func.__name__, str(e), duration)
            raise
    
    import inspect
    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


if __name__ == "__main__":
    # Teste do sistema de logging
    logger = get_logger("test")
    
    logger.info("Sistema de logging inicializado")
    logger.debug("Mensagem de debug", {"test_data": "valor"})
    logger.warning("Aviso de teste")
    logger.error("Erro de teste", {"error_code": 500})
    
    # Testa logs específicos
    logger.automation_start("test_action")
    logger.browser_event("page_loaded", "https://example.com")
    logger.security_event("stealth_enabled")
    logger.performance_metric("page_load_time", 1.5, "s")
    logger.user_interaction("click", "button#submit")
    logger.automation_success("test_action", 2.3)
    
    print("✅ Teste de logging concluído. Verifique os arquivos em 'logs/'.")
