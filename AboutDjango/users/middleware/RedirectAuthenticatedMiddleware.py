from django.shortcuts import redirect

class RedirectAuthenticatedMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated and request.path in ['/login/', '/register/']:  # Specify paths to check
            return redirect('polls:dashboard')  # Redirect to the desired URL
        
        # Process the request and get the response
        response = self.get_response(request)
        return response