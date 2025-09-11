"""
YouTube Automator - Automação Integrada do YouTube
================================================

Automator principal que integra todos os componentes modularizados.
"""

import asyncio
import os
import random
from typing import Dict, Any, Optional
from pathlib import Path

from ..core.browser_manager import BrowserManager
from ..automation.login_handler import YouTubeLoginHandler
from ..automation.human_simulator import HumanBehaviorSimulator
from ..utils.screenshot_manager import ScreenshotManager
from ..utils.logger import AutomationLogger
from ..utils.config import ConfigManager


class YouTubeAutomator:
    """Automator principal integrado para YouTube"""
    
    def __init__(self, profile_name: str = "youtube_stealth"):
        self.profile_name = profile_name
        self.browser_manager = BrowserManager(profile_name)
        self.login_handler = None
        self.human_simulator = None
        self.screenshot_manager = ScreenshotManager()
        self.logger = AutomationLogger("youtube_automator")
        self.config = ConfigManager()
        
        # Estado da automação
        self.is_running = False
        self.current_step = "initializing"
        
    async def initialize(self) -> bool:
        """Inicializa todos os componentes"""
        try:
            self.logger.info("🤖 Inicializando YouTube Automator...")
            
            # Lança browser stealth
            browser, page = await self.browser_manager.launch_stealth_browser(headless=True)
            
            # Inicializa componentes com a página
            self.login_handler = YouTubeLoginHandler(self.browser_manager)
            self.human_simulator = HumanBehaviorSimulator()
            
            # Captura screenshot inicial
            await self.screenshot_manager.capture_screenshot(
                page, "01_automator_initialized"
            )
            
            self.is_running = True
            self.current_step = "ready"
            
            self.logger.info("✅ YouTube Automator inicializado com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro na inicialização: {e}")
            await self.cleanup()
            return False
    
    async def execute_full_automation(self, email: str, password: str) -> bool:
        """Executa automação completa do YouTube"""
        try:
            if not self.is_running:
                self.logger.error("❌ Automator não foi inicializado")
                return False
            
            # Passo 1: Navegar para YouTube
            success = await self._navigate_to_youtube()
            if not success:
                return False
            
            # Passo 2: Fazer login
            success = await self._perform_login(email, password)
            if not success:
                return False
            
            # Passo 3: Explorar o YouTube
            success = await self._explore_youtube()
            if not success:
                return False
            
            # Passo 4: Simular atividade humana
            success = await self._simulate_human_activity()
            if not success:
                return False
            
            self.logger.info("🎉 Automação completa executada com sucesso!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro na automação: {e}")
            return False
        finally:
            await self.cleanup()
    
    async def _navigate_to_youtube(self) -> bool:
        """Navega para o YouTube"""
        try:
            self.current_step = "navigating_to_youtube"
            self.logger.info("📺 Navegando para YouTube...")
            
            success = await self.browser_manager.navigate_safely("https://www.youtube.com")
            if not success:
                return False
            
            await self.screenshot_manager.capture_screenshot(
                self.browser_manager.page, "02_youtube_homepage"
            )
            
            # Simula leitura da página
            await self.human_simulator.simulate_reading_page(duration_range=(3, 6))
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao navegar para YouTube: {e}")
            return False
    
    async def _perform_login(self, email: str, password: str) -> bool:
        """Executa processo de login"""
        try:
            self.current_step = "performing_login"
            self.logger.info("🔐 Iniciando processo de login...")
            
            # Encontra e clica no botão de login
            login_button = await self.browser_manager.page.wait_for_selector(
                'a[aria-label*="Sign in"], a[href*="accounts.google.com"]',
                timeout=10000
            )
            
            if login_button:
                await self.human_simulator.click_element_naturally(login_button)
                await self.screenshot_manager.capture_screenshot(
                    self.browser_manager.page, "03_login_button_clicked"
                )
            
            # Executa login com Google
            from ..automation.login_handler import LoginStrategy
            success = await self.login_handler.login(LoginStrategy.AUTOMATIC_LOGIN)
            
            if success:
                await self.screenshot_manager.capture_screenshot(
                    self.browser_manager.page, "04_login_successful"
                )
                self.logger.info("✅ Login realizado com sucesso")
                return True
            else:
                self.logger.error("❌ Falha no login")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro no processo de login: {e}")
            return False
    
    async def _explore_youtube(self) -> bool:
        """Explora o YouTube de forma natural"""
        try:
            self.current_step = "exploring_youtube"
            self.logger.info("🔍 Explorando YouTube...")
            
            # Volta para página principal se necessário
            current_url = self.browser_manager.page.url
            if "youtube.com" not in current_url:
                await self.browser_manager.navigate_safely("https://www.youtube.com")
            
            # Simula scroll na página principal
            await self.human_simulator.smooth_scroll_page(scroll_percentage=30)
            await asyncio.sleep(random.uniform(2, 4))
            
            # Captura screenshot da exploração
            await self.screenshot_manager.capture_screenshot(
                self.browser_manager.page, "05_youtube_exploration"
            )
            
            # Navega para trending
            try:
                trending_link = await self.browser_manager.page.wait_for_selector(
                    'a[title="Trending"], a[href*="/feed/trending"]',
                    timeout=5000
                )
                if trending_link:
                    await self.human_simulator.click_element_naturally(trending_link)
                    await asyncio.sleep(random.uniform(3, 5))
                    
                    await self.screenshot_manager.capture_screenshot(
                        self.browser_manager.page, "06_trending_page"
                    )
            except:
                self.logger.info("⚠️ Link Trending não encontrado, continuando...")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro na exploração: {e}")
            return False
    
    async def _simulate_human_activity(self) -> bool:
        """Simula atividade humana natural"""
        try:
            self.current_step = "simulating_activity"
            self.logger.info("👤 Simulando atividade humana...")
            
            # Movimento de mouse aleatório
            await self.human_simulator.random_mouse_movement(duration=3)
            
            # Scroll suave
            await self.human_simulator.smooth_scroll_page(scroll_percentage=50)
            
            # Pausa para "leitura"
            await self.human_simulator.simulate_reading_page(duration_range=(5, 10))
            
            # Screenshot final
            await self.screenshot_manager.capture_screenshot(
                self.browser_manager.page, "07_final_activity"
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro na simulação de atividade: {e}")
            return False
    
    async def cleanup(self):
        """Limpa todos os recursos"""
        try:
            self.logger.info("🧹 Limpando recursos do automator...")
            
            if self.browser_manager:
                await self.browser_manager.cleanup()
            
            if self.screenshot_manager:
                await self.screenshot_manager.cleanup_old_screenshots()
            
            self.is_running = False
            self.current_step = "cleaned"
            
            self.logger.info("✅ Limpeza concluída")
            
        except Exception as e:
            self.logger.error(f"⚠️ Erro na limpeza: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status atual da automação"""
        return {
            "is_running": self.is_running,
            "current_step": self.current_step,
            "profile_name": self.profile_name,
            "browser_active": self.browser_manager.browser is not None
        }