"""
Emergency Fix - Correção Imediata para Problemas de Detecção
============================================================

Script de emergência para contornar detecção do Google com login manual assistido.
"""

import asyncio
import random
import os
import sys
from pathlib import Path

# Adiciona src ao path para imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    import nodriver as uc
except ImportError:
    print("❌ nodriver não encontrado. Execute: pip install nodriver")
    sys.exit(1)

from src.core.browser_manager import BrowserManager
from src.automation.login_handler import YouTubeLoginHandler, LoginStrategy, LoginResult
from src.automation.human_simulator import HumanBehaviorSimulator
from src.security.credential_manager import CredentialManager


class YouTubeStealthAutomator:
    """Automator de emergência com máxima furtividade"""
    
    def __init__(self):
        self.browser_manager = None
        self.login_handler = None
        self.human_simulator = HumanBehaviorSimulator()
        self.credential_manager = CredentialManager()
    
    async def launch_stealth_browser(self):
        """Lança browser com máxima furtividade"""
        print("🚀 Iniciando browser stealth de emergência...")
        
        self.browser_manager = BrowserManager(profile_name="emergency_stealth")
        browser, page = await self.browser_manager.launch_stealth_browser(
            headless=False,
            context_rotation=True
        )
        
        self.login_handler = YouTubeLoginHandler(self.browser_manager, self.credential_manager)
        
        print("✅ Browser stealth configurado")
        return browser, page
    
    async def smart_login_strategy(self):
        """Estratégia inteligente de login - prioriza manual assistido"""
        
        print("\n🔐 ESTRATÉGIA DE LOGIN INTELIGENTE")
        print("=" * 50)
        
        # Estratégia 1: Verificar sessão existente
        print("🔄 Verificando sessão existente...")
        result = await self.login_handler.login(LoginStrategy.SESSION_RESTORE)
        
        if result == LoginResult.SUCCESS:
            print("✅ Login via sessão existente - SUCESSO!")
            return True
        
        # Estratégia 2: Login manual assistido (mais seguro contra detecção)
        print("\n🛡️  Usando login manual assistido para evitar detecção...")
        result = await self.login_handler.login(LoginStrategy.MANUAL_ASSISTED)
        
        if result == LoginResult.SUCCESS:
            print("✅ Login manual assistido - SUCESSO!")
            return True
        
        # Estratégia 3: Tentativa automática como último recurso
        print("\n🤖 Tentando login automático como último recurso...")
        result = await self.login_handler.login(LoginStrategy.AUTOMATIC_LOGIN)
        
        if result == LoginResult.SUCCESS:
            print("✅ Login automático - SUCESSO!")
            return True
        
        print("❌ Todas as estratégias de login falharam")
        return False
    
    async def simulate_human_browsing(self):
        """Simula navegação humana para estabelecer credibilidade"""
        
        print("\n🎭 Simulando comportamento humano...")
        
        page = self.browser_manager.page
        
        # Simula leitura da página inicial
        await self.human_simulator.simulate_reading_pause(200)
        
        # Movimento aleatório do mouse
        await self.human_simulator.random_mouse_movement(page)
        
        # Scroll exploratório
        await self.human_simulator.human_scroll(page, 'down', random.randint(2, 4))
        await asyncio.sleep(random.uniform(1.0, 3.0))
        await self.human_simulator.human_scroll(page, 'up', random.randint(1, 2))
        
        # Simula verificação de notificações/trending
        try:
            trending_element = await page.find('a[title*="Trending"]', timeout=5000)
            if trending_element:
                print("📈 Navegando para Trending...")
                await self.human_simulator.human_click(page, trending_element)
                await self.human_simulator.simulate_reading_pause(150)
                
                # Volta para página inicial
                await asyncio.sleep(random.uniform(2.0, 4.0))
                await page.goto('https://www.youtube.com')
                
        except Exception as e:
            print(f"⚠️  Navegação para trending falhou: {e}")
        
        print("✅ Simulação de comportamento humano concluída")
    
    async def verify_stealth_status(self):
        """Verifica se o stealth está funcionando"""
        
        print("\n🛡️  Verificando status de furtividade...")
        
        page = self.browser_manager.page
        
        # Testa detecção de webdriver
        webdriver_detected = await page.evaluate('navigator.webdriver')
        
        if webdriver_detected:
            print("⚠️  ALERTA: navigator.webdriver detectado!")
        else:
            print("✅ navigator.webdriver: não detectado")
        
        # Verifica user agent
        user_agent = await page.evaluate('navigator.userAgent')
        if 'HeadlessChrome' in user_agent or 'Automation' in user_agent:
            print("⚠️  ALERTA: User agent suspeito!")
        else:
            print("✅ User agent: aparenta ser normal")
        
        # Verifica plugins
        plugins_count = await page.evaluate('navigator.plugins.length')
        print(f"🔌 Plugins detectados: {plugins_count}")
        
        # Verifica se está sendo detectado como bot
        page_source = await page.content()
        bot_indicators = ['bot detected', 'automation detected', 'please verify', 'captcha']
        
        detected_indicators = [indicator for indicator in bot_indicators if indicator.lower() in page_source.lower()]
        
        if detected_indicators:
            print(f"⚠️  ALERTA: Possível detecção de bot: {detected_indicators}")
        else:
            print("✅ Nenhum indicador de detecção de bot encontrado")
        
        return len(detected_indicators) == 0
    
    async def run_emergency_automation(self):
        """Executa automação de emergência completa"""
        
        print("\n" + "="*60)
        print("🚨 YOUTUBE STEALTH AUTOMATOR - EMERGÊNCIA")
        print("="*60)
        print("🎯 Objetivo: Login seguro evitando detecção do Google")
        print("🛡️  Estratégia: Máxima furtividade + Login manual assistido")
        print("="*60)
        
        try:
            # 1. Lança browser stealth
            browser, page = await self.launch_stealth_browser()
            
            # 2. Verifica status de furtividade
            stealth_ok = await self.verify_stealth_status()
            
            if not stealth_ok:
                print("⚠️  Stealth pode estar comprometido, mas continuando...")
            
            # 3. Executa login inteligente
            login_success = await self.smart_login_strategy()
            
            if not login_success:
                print("❌ Falha no login - encerrando")
                return False
            
            # 4. Simula comportamento humano pós-login
            await self.simulate_human_browsing()
            
            # 5. Captura screenshot de confirmação
            screenshot_path = await self.browser_manager.take_screenshot("login_success.png")
            
            print("\n🎉 AUTOMAÇÃO DE EMERGÊNCIA CONCLUÍDA COM SUCESSO!")
            print(f"📸 Screenshot salvo: {screenshot_path}")
            print("\n🔄 O browser permanecerá aberto para uso manual...")
            print("🔒 Pressione Ctrl+C para encerrar")
            
            # Mantém browser aberto para uso manual
            try:
                while True:
                    await asyncio.sleep(10)
                    # Verifica se ainda está logado
                    if not await self.login_handler._is_logged_in():
                        print("⚠️  Sessão perdida detectada")
                        break
            except KeyboardInterrupt:
                print("\n🔒 Encerrando por solicitação do usuário...")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro crítico na automação: {e}")
            return False
        
        finally:
            if self.browser_manager:
                await self.browser_manager.close_browser(save_session=True)


async def main():
    """Função principal de emergência"""
    
    # Verifica dependências
    try:
        import nodriver
    except ImportError:
        print("❌ Dependência crítica não encontrada!")
        print("📦 Execute: pip install nodriver")
        return
    
    # Executa automação de emergência
    automator = YouTubeStealthAutomator()
    success = await automator.run_emergency_automation()
    
    if success:
        print("\n✅ Automação de emergência executada com sucesso!")
        print("🔐 Sessão salva para próximas execuções")
    else:
        print("\n❌ Automação de emergência falhou")
        print("💡 Dicas:")
        print("   - Verifique sua conexão com a internet")
        print("   - Tente executar novamente")
        print("   - Use VPN se necessário")


if __name__ == "__main__":
    print("🚨 YOUTUBE STEALTH AUTOMATOR - MODO EMERGÊNCIA")
    print("🛡️  Proteção máxima contra detecção do Google")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🔒 Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        print("🔧 Verifique as dependências e tente novamente")
