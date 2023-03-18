# middleware.py

import secrets

class SetUserIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('user_id'):
            request.session['user_id'] = secrets.token_hex(5)
        response = self.get_response(request)
        return response