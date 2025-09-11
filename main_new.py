"""
YouTube Automation - Main Entry Point
=====================================

Ponto de entrada principal usando arquitetura modular com Playwright.
Refatorado para máxima compatibilidade em containers e ambientes CI/CD.
"""

import asyncio
import os
import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.automation.youtube_automator import YouTubeAutomator
from src.utils.logger import AutomationLogger
from src.utils.config import ConfigManager


async def main():
    """Função principal da automação"""
    
    # Configuração inicial
    logger = AutomationLogger("main")
    config = ConfigManager()
    
    logger.info("🤖 Iniciando automação stealth do YouTube...")
    
    # Limpa screenshots antigos
    from src.utils.screenshot_manager import ScreenshotManager
    screenshot_manager = ScreenshotManager()
    await screenshot_manager.cleanup_old_screenshots()
    
    # Credenciais (em produção, usar variáveis de ambiente)
    email = os.getenv("GOOGLE_EMAIL", "seu_email@gmail.com")
    password = os.getenv("GOOGLE_PASSWORD", "sua_senha")
    
    if email == "seu_email@gmail.com" or password == "sua_senha":
        logger.warning("⚠️ Usando credenciais padrão. Configure GOOGLE_EMAIL e GOOGLE_PASSWORD")
    
    # Instancia automator
    automator = YouTubeAutomator("stealth_profile_v2")
    
    try:
        # Inicializa automator
        success = await automator.initialize()
        if not success:
            logger.error("❌ Falha na inicialização do automator")
            return False
        
        # Executa automação completa
        logger.info("🚀 Executando automação completa...")
        success = await automator.execute_full_automation(email, password)
        
        if success:
            logger.info("🎉 Automação concluída com sucesso!")
            return True
        else:
            logger.error("❌ Automação falhou")
            return False
            
    except KeyboardInterrupt:
        logger.info("⏹️ Automação interrompida pelo usuário")
        return False
    except Exception as e:
        logger.error(f"❌ Erro durante a execução: {e}")
        return False
    finally:
        logger.info("🔚 Finalizando automação...")
        await automator.cleanup()
        logger.info("🧹 Limpeza final de screenshots...")
        await screenshot_manager.cleanup_old_screenshots()


if __name__ == "__main__":
    # Executa automação
    success = asyncio.run(main())
    
    # Código de saída
    exit_code = 0 if success else 1
    sys.exit(exit_code)