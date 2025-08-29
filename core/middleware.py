import logging

logger = logging.getLogger(__name__)

class SessionDebugMiddleware:
    """Middleware para debug de sessões"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Antes da requisição
        print(f"🔍 === MIDDLEWARE SESSION DEBUG ===")
        print(f"📊 Path: {request.path}")
        print(f"📊 Session key: {request.session.session_key}")
        print(f"📊 Session data: {dict(request.session)}")
        print(f"📊 Session modified: {request.session.modified}")
        
        # Processar a requisição
        response = self.get_response(request)
        
        # Depois da requisição
        print(f"📊 Response status: {response.status_code}")
        print(f"📊 Session data após: {dict(request.session)}")
        print(f"📊 Session modified após: {request.session.modified}")
        print(f"===============================")
        
        return response
