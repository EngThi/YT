"""
Browser Manager - Gerenciamento Stealth do Browser
==================================================

Gerenciador avançado de browser com recursos de stealth e anti-detecção.
Refatorado para usar Playwright com máxima compatibilidade em containers.
"""

import asyncio
import json
import os
import random
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from playwright.async_api import (Browser, BrowserContext, Page,
                                      async_playwright)
    from playwright_stealth import stealth_async
except ImportError:
    print("⚠️  Playwright não encontrado. Execute: pip install playwright playwright-stealth")
    async_playwright = None

from ..security.fingerprint_spoofing import (AdvancedStealthEngine,
                                             ContextRotator)


class BrowserManager:
    """Gerenciador avançado de browser stealth com Playwright"""
    
    def __init__(self, profile_name: str = "default"):
        self.profile_name = profile_name
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.stealth_engine = AdvancedStealthEngine()
        self.context_rotator = ContextRotator()
        self.profile_dir = self._get_profile_directory()
        
    def _get_profile_directory(self) -> str:
        """Retorna diretório do profile"""
        profiles_dir = Path("browser_profiles")
        profiles_dir.mkdir(exist_ok=True)
        return str(profiles_dir / self.profile_name)
    
    async def launch_stealth_browser(self, headless: bool = True, 
                                   context_rotation: bool = True) -> tuple:
        """Lança browser com máxima furtividade usando Playwright"""
        
        try:
            if async_playwright is None:
                raise ImportError("Playwright não está disponível")
            
            # Seleciona contexto (rotação ou aleatório)
            if context_rotation:
                context = self.context_rotator.get_next_context()
                profile_dir = os.path.join(self.profile_dir, context['profile_dir'])
            else:
                profile_dir = self.profile_dir
            
            # Configurações stealth do browser
            fingerprint = await self.stealth_engine.setup_realistic_browser()
            
            print(f"🚀 Lançando browser stealth com Playwright (Profile: {profile_dir})")
            
            # Inicia Playwright
            self.playwright = await async_playwright().start()
            
            # Argumentos customizados para máxima furtividade em containers
            browser_args = [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-sync',
                '--disable-default-apps',
                '--disable-background-networking',
                '--disable-client-side-phishing-detection',
                '--mute-audio',
                '--no-first-run',
                '--disable-gpu',
                '--disable-software-rasterizer'
            ]
            
            # Lança browser Chromium
            self.browser = await self.playwright.chromium.launch(
                headless=headless,
                args=browser_args,
                chromium_sandbox=False
            )
            
            # Cria contexto com fingerprint
            self.context = await self.browser.new_context(
                user_agent=fingerprint["user_agent"],
                viewport={
                    'width': fingerprint["viewport"]["width"],
                    'height': fingerprint["viewport"]["height"]
                },
                locale=fingerprint['language'].split(',')[0],
                timezone_id=fingerprint['timezone'],
                geolocation=fingerprint.get('geolocation'),
                permissions=['geolocation'] if fingerprint.get('geolocation') else []
            )
            
            # Cria página
            self.page = await self.context.new_page()
            
            # Aplica stealth
            await stealth_async(self.page)
            
            # Aplica scripts de stealth adicionais
            await self.stealth_engine.inject_stealth_scripts(self.page)
            
            print("✅ Browser stealth Playwright configurado com sucesso")
            return self.browser, self.page
            
        except Exception as e:
            print(f"❌ Erro ao lançar browser Playwright: {e}")
            await self.cleanup()
            raise
    
    async def _setup_browser_fingerprint(self, fingerprint: Dict[str, Any]):
        """Configura fingerprint completo do browser"""
        
        # Define timezone
        await self.page.emulate_timezone(fingerprint['timezone'])
        
        # Define localização
        if 'geolocation' in fingerprint:
            await self.page.emulate_geolocation(
                latitude=fingerprint['geolocation']['latitude'],
                longitude=fingerprint['geolocation']['longitude'],
                accuracy=fingerprint['geolocation']['accuracy']
            )
        
        # Injeta scripts adicionais de fingerprint
        await self.page.evaluate(f"""
            // Override screen properties
            Object.defineProperty(screen, 'width', {{
                get: () => {fingerprint['viewport']['width']}
            }});
            Object.defineProperty(screen, 'height', {{
                get: () => {fingerprint['viewport']['height']}
            }});
            Object.defineProperty(screen, 'availWidth', {{
                get: () => {fingerprint['viewport']['width']}
            }});
            Object.defineProperty(screen, 'availHeight', {{
                get: () => {fingerprint['viewport']['height'] - 40}
            }});
            
            // Override language
            Object.defineProperty(navigator, 'language', {{
                get: () => '{fingerprint['language'].split(',')[0]}'
            }});
            
            // Override platform
            Object.defineProperty(navigator, 'platform', {{
                get: () => '{fingerprint['platform']}'
            }});
            
            // Mock battery API
            Object.defineProperty(navigator, 'getBattery', {{
                get: () => () => Promise.resolve({{
                    charging: true,
                    chargingTime: 0,
                    dischargingTime: Infinity,
                    level: {random.uniform(0.8, 1.0)}
                }})
            }});
        """)
    
    async def cleanup(self):
        """Limpa recursos do browser"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            print("🧹 Recursos do browser limpos")
        except Exception as e:
            print(f"⚠️ Erro na limpeza: {e}")
    
    async def navigate_safely(self, url: str, wait_for: str = "domcontentloaded",
                            timeout: int = 30000) -> bool:
        """Navega para URL com verificações de segurança"""
        try:
            print(f"🌐 Navegando para: {url}")
            
            # Adiciona delay humano antes da navegação
            await asyncio.sleep(random.uniform(1.0, 3.0))
            
            # Navega para a URL
            await self.page.goto(url, wait_until=wait_for, timeout=timeout)
            
            # Verifica se a página carregou corretamente
            await self._verify_page_load()
            
            # Pequena pausa após carregamento
            await asyncio.sleep(random.uniform(2.0, 4.0))
            
            print("✅ Navegação concluída com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro na navegação: {e}")
            return False
    
    async def _verify_page_load(self):
        """Verifica se a página carregou adequadamente"""
        try:
            # Aguarda o documento estar pronto
            await self.page.wait_for_function("document.readyState === 'complete'", timeout=10000)
            
            # Verifica se não há erros visíveis
            error_indicators = [
                'text="This page isn\'t working"',
                'text="Something went wrong"',
                'text="Access denied"',
                'class*="error"',
                'id*="error"'
            ]
            
            for indicator in error_indicators:
                try:
                    error_element = await self.page.find(indicator, timeout=1000)
                    if error_element:
                        print(f"⚠️  Possível erro detectado na página: {indicator}")
                        break
                except:
                    continue  # Sem erro encontrado, continua
                    
        except Exception as e:
            print(f"⚠️  Não foi possível verificar carregamento da página: {e}")
    
    async def take_screenshot(self, filename: str = None, full_page: bool = False) -> str:
        """Captura screenshot com nome automático"""
        try:
            if not filename:
                timestamp = int(asyncio.get_event_loop().time())
                filename = f"screenshot_{timestamp}.png"
            
            screenshots_dir = Path("temp_screenshots")
            screenshots_dir.mkdir(exist_ok=True)
            
            screenshot_path = screenshots_dir / filename
            
            await self.page.screenshot(
                path=str(screenshot_path),
                full_page=full_page
            )
            
            print(f"📸 Screenshot salvo: {screenshot_path}")
            return str(screenshot_path)
            
        except Exception as e:
            print(f"❌ Erro ao capturar screenshot: {e}")
            return ""
    
    async def get_page_info(self) -> Dict[str, Any]:
        """Obtém informações da página atual"""
        try:
            info = {
                'url': self.page.url,
                'title': await self.page.title(),
                'ready_state': await self.page.evaluate('document.readyState'),
                'viewport': await self.page.evaluate('({width: window.innerWidth, height: window.innerHeight})'),
                'user_agent': await self.page.evaluate('navigator.userAgent'),
                'cookies_count': len(await self.page.cookies()),
                'timestamp': asyncio.get_event_loop().time()
            }
            return info
        except Exception as e:
            print(f"❌ Erro ao obter informações da página: {e}")
            return {}
    
    async def clear_browser_data(self, clear_cookies: bool = True, 
                               clear_cache: bool = True,
                               clear_local_storage: bool = True):
        """Limpa dados do browser"""
        try:
            if clear_local_storage:
                await self.page.evaluate("""
                    localStorage.clear();
                    sessionStorage.clear();
                """)
            
            if clear_cookies:
                cookies = await self.page.cookies()
                for cookie in cookies:
                    await self.page.delete_cookie(cookie['name'])
            
            print("🧹 Dados do browser limpos")
            
        except Exception as e:
            print(f"❌ Erro ao limpar dados: {e}")
    
    async def close_browser(self, save_session: bool = True):
        """Fecha browser com opção de salvar sessão"""
        try:
            if save_session and self.page:
                # Salva cookies da sessão
                cookies = await self.page.cookies()
                session_file = Path(self.profile_dir) / "last_session.json"
                
                session_data = {
                    'cookies': cookies,
                    'url': self.page.url,
                    'timestamp': asyncio.get_event_loop().time()
                }
                
                with open(session_file, 'w') as f:
                    json.dump(session_data, f, indent=2)
                
                print("💾 Sessão salva")
            
            if self.browser:
                await self.browser.close()
                print("🔒 Browser fechado")
                
        except Exception as e:
            print(f"❌ Erro ao fechar browser: {e}")
    
    async def restore_session(self) -> bool:
        """Restaura sessão anterior"""
        try:
            session_file = Path(self.profile_dir) / "last_session.json"
            
            if not session_file.exists():
                print("📝 Nenhuma sessão anterior encontrada")
                return False
            
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            # Verifica se a sessão não é muito antiga (24 horas)
            current_time = asyncio.get_event_loop().time()
            session_age = current_time - session_data.get('timestamp', 0)
            
            if session_age > 86400:  # 24 horas
                print("⏰ Sessão muito antiga, iniciando nova sessão")
                return False
            
            # Restaura cookies
            if 'cookies' in session_data:
                await self.page.add_cookies(session_data['cookies'])
            
            # Navega para última URL (opcional)
            if 'url' in session_data and session_data['url'] != 'about:blank':
                await self.navigate_safely(session_data['url'])
            
            print("🔄 Sessão restaurada com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao restaurar sessão: {e}")
            return False
    
    def __enter__(self):
        """Context manager support"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup"""
        if self.browser:
            asyncio.create_task(self.close_browser())


# Factory function para criar browser manager
def create_browser_manager(profile: str = "default") -> BrowserManager:
    """Factory para criar BrowserManager"""
    return BrowserManager(profile_name=profile)
