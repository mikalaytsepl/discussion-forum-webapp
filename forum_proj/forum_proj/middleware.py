class ExtraSecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response["Cross-Origin-Resource-Policy"] = "same-site"
        response["Cross-Origin-Opener-Policy"] = "same-origin"

        return response
