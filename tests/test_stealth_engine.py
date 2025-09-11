"""
Testes para Stealth Engine
==========================

Testes unitários para o módulo de anti-detecção.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.security.fingerprint_spoofing import AdvancedStealthEngine, ContextRotator


class TestAdvancedStealthEngine:
    """Testes para AdvancedStealthEngine"""
    
    def test_initialization(self):
        """Testa inicialização do engine"""
        engine = AdvancedStealthEngine()
        
        assert engine.brazilian_fingerprints is not None
        assert len(engine.brazilian_fingerprints) >= 3
        assert engine.current_fingerprint is None
    
    def test_select_random_fingerprint(self):
        """Testa seleção de fingerprint aleatório"""
        engine = AdvancedStealthEngine()
        
        fingerprint = engine.select_random_fingerprint()
        
        assert fingerprint is not None
        assert engine.current_fingerprint == fingerprint
        assert fingerprint.user_agent is not None
        assert "pt-BR" in fingerprint.language
        assert fingerprint.timezone == "America/Sao_Paulo"
    
    @pytest.mark.asyncio
    async def test_setup_realistic_browser(self):
        """Testa configuração de browser realista"""
        engine = AdvancedStealthEngine()
        
        options = await engine.setup_realistic_browser()
        
        assert "user_agent" in options
        assert "viewport" in options
        assert "language" in options
        assert "timezone" in options
        assert options["timezone"] == "America/Sao_Paulo"
        assert "pt-BR" in options["language"]
    
    def test_get_human_headers(self):
        """Testa geração de headers humanos"""
        engine = AdvancedStealthEngine()
        
        headers = engine._get_human_headers()
        
        assert "Accept" in headers
        assert "Accept-Language" in headers
        assert "pt-BR" in headers["Accept-Language"]
    
    def test_get_brazilian_geolocation(self):
        """Testa geolocalização brasileira"""
        engine = AdvancedStealthEngine()
        
        geo = engine._get_brazilian_geolocation()
        
        assert "latitude" in geo
        assert "longitude" in geo
        assert "accuracy" in geo
        
        # Verifica se está aproximadamente no Brasil
        assert -35.0 <= geo["latitude"] <= -5.0
        assert -75.0 <= geo["longitude"] <= -30.0
    
    def test_get_stealth_browser_args(self):
        """Testa argumentos stealth do browser"""
        engine = AdvancedStealthEngine()
        
        args = engine.get_stealth_browser_args()
        
        assert isinstance(args, list)
        assert len(args) > 10
        assert "--disable-blink-features=AutomationControlled" in args
        assert "--no-first-run" in args


class TestContextRotator:
    """Testes para ContextRotator"""
    
    def test_initialization(self):
        """Testa inicialização do rotator"""
        rotator = ContextRotator()
        
        assert rotator.browser_contexts is not None
        assert len(rotator.browser_contexts) >= 3
        assert rotator.current_context_index == 0
    
    def test_get_next_context(self):
        """Testa rotação sequencial de contextos"""
        rotator = ContextRotator()
        
        first_context = rotator.get_next_context()
        second_context = rotator.get_next_context()
        
        assert first_context != second_context
        assert rotator.current_context_index == 2
        
        # Testa wrap-around
        for _ in range(len(rotator.browser_contexts)):
            rotator.get_next_context()
        
        assert rotator.current_context_index == 2  # Voltou ao início + 2
    
    def test_get_random_context(self):
        """Testa seleção aleatória de contexto"""
        rotator = ContextRotator()
        
        context = rotator.get_random_context()
        
        assert context in rotator.browser_contexts
        assert "os" in context
        assert "browser" in context
        assert "profile_dir" in context
    
    def test_context_structure(self):
        """Testa estrutura dos contextos"""
        rotator = ContextRotator()
        
        for context in rotator.browser_contexts:
            assert "os" in context
            assert "browser" in context
            assert "resolution" in context
            assert "timezone" in context
            assert "profile_dir" in context
            assert context["timezone"] == "America/Sao_Paulo"


@pytest.mark.asyncio
async def test_stealth_engine_integration():
    """Teste de integração do stealth engine"""
    engine = AdvancedStealthEngine()
    rotator = ContextRotator()
    
    # Seleciona contexto
    context = rotator.get_random_context()
    
    # Configura browser
    options = await engine.setup_realistic_browser()
    
    # Verifica compatibilidade
    assert options["timezone"] == "America/Sao_Paulo"
    assert context["timezone"] == "America/Sao_Paulo"
    
    # Simula injeção de scripts (mock)
    mock_page = Mock()
    mock_page.evaluate = AsyncMock()
    
    await engine.inject_stealth_scripts(mock_page)
    
    # Verifica se foi chamado
    mock_page.evaluate.assert_called_once()


if __name__ == "__main__":
    # Executa testes se chamado diretamente
    pytest.main([__file__, "-v"])
