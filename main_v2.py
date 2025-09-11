"""
YouTube Automation - Entry Point Principal
==========================================

Sistema profissional de automação YouTube com arquitetura modular e stealth avançado.
"""

import asyncio
import sys
import argparse
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.core.browser_manager import BrowserManager
    from src.automation.login_handler import YouTubeLoginHandler, LoginStrategy
    from src.automation.human_simulator import HumanBehaviorSimulator
    from src.security.credential_manager import CredentialManager
    from src.utils.logger import get_logger, LogLevel
    from src.utils.config import setup_project, get_config
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("🔧 Execute primeiro: pip install -r requirements.txt")
    sys.exit(1)


class YouTubeAutomationApp:
    """Aplicação principal de automação YouTube"""
    
    def __init__(self, profile: str = "default", headless: bool = False):
        self.profile = profile
        self.headless = headless
        
        # Configura logging
        self.logger = get_logger("yt_automation")
        
        # Carrega configurações
        self.config = get_config()
        
        # Inicializa componentes
        self.browser_manager = None
        self.login_handler = None
        self.human_simulator = HumanBehaviorSimulator()
        self.credential_manager = CredentialManager()
    
    async def initialize(self):
        """Inicializa a aplicação"""
        self.logger.info("🚀 Inicializando YouTube Automation v2.0")
        
        try:
            # Configura browser manager
            self.browser_manager = BrowserManager(profile_name=self.profile)
            
            # Lança browser stealth
            browser, page = await self.browser_manager.launch_stealth_browser(
                headless=self.headless,
                context_rotation=self.config.browser.context_rotation
            )
            
            # Configura login handler
            self.login_handler = YouTubeLoginHandler(
                self.browser_manager, 
                self.credential_manager
            )
            
            self.logger.info("✅ Aplicação inicializada com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro na inicialização: {e}", exc_info=True)
            return False
    
    async def run_automation(self, strategy: str = "hybrid"):
        """Executa automação principal"""
        
        try:
            # Mapeia estratégias
            strategy_map = {
                "session": LoginStrategy.SESSION_RESTORE,
                "auto": LoginStrategy.AUTOMATIC_LOGIN,
                "manual": LoginStrategy.MANUAL_ASSISTED,
                "hybrid": LoginStrategy.HYBRID_APPROACH
            }
            
            login_strategy = strategy_map.get(strategy, LoginStrategy.HYBRID_APPROACH)
            
            self.logger.automation_start("youtube_automation", f"strategy: {strategy}")
            
            # Executa login
            login_result = await self.login_handler.login(login_strategy)
            
            if login_result.value != "success":
                self.logger.automation_failure("login", f"Login falhou: {login_result.value}")
                return False
            
            # Simula comportamento humano pós-login
            await self.simulate_human_behavior()
            
            # Executa automação específica (customizável)
            await self.execute_custom_automation()
            
            self.logger.automation_success("youtube_automation")
            return True
            
        except Exception as e:
            self.logger.automation_failure("youtube_automation", str(e))
            return False
    
    async def simulate_human_behavior(self):
        """Simula comportamento humano realista"""
        self.logger.info("🎭 Simulando comportamento humano...")
        
        page = self.browser_manager.page
        
        # Pausa inicial para "ler" a página
        await self.human_simulator.simulate_reading_pause(200)
        
        # Movimentos aleatórios do mouse
        await self.human_simulator.random_mouse_movement(page)
        
        # Scroll exploratório
        await self.human_simulator.human_scroll(page, 'down', 3)
        await asyncio.sleep(2.0)
        await self.human_simulator.human_scroll(page, 'up', 1)
        
        self.logger.info("✅ Simulação de comportamento humano concluída")
    
    async def execute_custom_automation(self):
        """Executa automação customizada - SOBRESCREVER CONFORME NECESSÁRIO"""
        self.logger.info("🔧 Executando automação personalizada...")
        
        # Placeholder para automação específica
        # Aqui você pode adicionar:
        # - Navegação para vídeos específicos
        # - Interações com comentários
        # - Coleta de dados
        # - Etc.
        
        page = self.browser_manager.page
        
        # Exemplo: Navegar para trending
        try:
            trending_link = await page.find('a[title*="Trending"]', timeout=5000)
            if trending_link:
                self.logger.user_interaction("click", "trending_link")
                await self.human_simulator.human_click(page, trending_link)
                await self.human_simulator.simulate_reading_pause(150)
            
        except Exception as e:
            self.logger.warning(f"Navegação para trending falhou: {e}")
        
        # Captura screenshot final
        screenshot_path = await self.browser_manager.take_screenshot("automation_complete.png")
        self.logger.info(f"📸 Screenshot salvo: {screenshot_path}")
    
    async def cleanup(self):
        """Limpeza final"""
        self.logger.info("🧹 Executando limpeza...")
        
        if self.browser_manager:
            await self.browser_manager.close_browser(save_session=True)
        
        self.logger.info("✅ Limpeza concluída")
    
    async def run(self, strategy: str = "hybrid", keep_open: bool = False):
        """Executa aplicação completa"""
        
        try:
            # Inicializa
            if not await self.initialize():
                return False
            
            # Executa automação
            success = await self.run_automation(strategy)
            
            if not success:
                self.logger.error("❌ Automação falhou")
                return False
            
            if keep_open:
                self.logger.info("🔄 Mantendo browser aberto para uso manual...")
                self.logger.info("🔒 Pressione Ctrl+C para encerrar")
                
                try:
                    while True:
                        await asyncio.sleep(10)
                        # Verificação periódica de saúde
                        if not await self.login_handler._is_logged_in():
                            self.logger.warning("⚠️ Sessão perdida detectada")
                            break
                except KeyboardInterrupt:
                    self.logger.info("🔒 Encerrando por solicitação do usuário")
            
            return True
            
        except Exception as e:
            self.logger.critical(f"❌ Erro crítico na aplicação: {e}", exc_info=True)
            return False
        
        finally:
            await self.cleanup()


def create_cli_parser():
    """Cria parser para CLI"""
    parser = argparse.ArgumentParser(
        description="YouTube Automation - Sistema Profissional de Automação",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  %(prog)s                           # Execução padrão (híbrida)
  %(prog)s --strategy manual         # Força login manual
  %(prog)s --strategy auto          # Tenta login automático
  %(prog)s --profile stealth        # Usa profile específico
  %(prog)s --headless               # Execução sem interface
  %(prog)s --keep-open              # Mantém browser aberto
  %(prog)s --setup                  # Configura projeto inicial
        """
    )
    
    parser.add_argument(
        "--strategy",
        choices=["session", "auto", "manual", "hybrid"],
        default="hybrid",
        help="Estratégia de login (padrão: hybrid)"
    )
    
    parser.add_argument(
        "--profile",
        default="default",
        help="Nome do profile do browser (padrão: default)"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Executa em modo headless (sem interface)"
    )
    
    parser.add_argument(
        "--keep-open",
        action="store_true",
        help="Mantém browser aberto após automação"
    )
    
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Executa configuração inicial do projeto"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Nível de logging (padrão: INFO)"
    )
    
    parser.add_argument(
        "--credentials",
        action="store_true",
        help="Configura credenciais interativamente"
    )
    
    return parser


async def main():
    """Função principal"""
    parser = create_cli_parser()
    args = parser.parse_args()
    
    # Banner
    print("=" * 60)
    print("🤖 YOUTUBE AUTOMATION v2.0 - SISTEMA PROFISSIONAL")
    print("=" * 60)
    print("🛡️  Anti-detecção avançada | 🎭 Simulação humana")
    print("🔐 Login inteligente | 📊 Logging estruturado")
    print("=" * 60)
    
    try:
        # Configuração inicial se solicitado
        if args.setup:
            print("\n🔧 Executando configuração inicial...")
            setup_project()
            print("✅ Configuração inicial concluída!")
            return
        
        # Configuração de credenciais se solicitado
        if args.credentials:
            print("\n🔐 Configurando credenciais...")
            cm = CredentialManager()
            if cm.setup_credentials_interactively():
                print("✅ Credenciais configuradas com sucesso!")
            else:
                print("❌ Falha na configuração de credenciais")
            return
        
        # Configura nível de logging
        logger = get_logger()
        if hasattr(LogLevel, args.log_level):
            from src.utils.logger import LogManager
            LogManager.set_global_level(getattr(LogLevel, args.log_level))
        
        # Executa aplicação
        app = YouTubeAutomationApp(
            profile=args.profile,
            headless=args.headless
        )
        
        success = await app.run(
            strategy=args.strategy,
            keep_open=args.keep_open
        )
        
        if success:
            print("\n🎉 AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
        else:
            print("\n❌ AUTOMAÇÃO FALHOU")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n🔒 Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Verifica dependências críticas
    try:
        import nodriver
    except ImportError:
        print("❌ Dependência crítica não encontrada!")
        print("📦 Execute: pip install -r requirements.txt")
        sys.exit(1)
    
    # Executa aplicação
    asyncio.run(main())
