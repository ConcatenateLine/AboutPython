from functools import wraps

def public_path(view_func):
    """
    Decorator to mark a view as public, meaning it does not require authentication.
    appends a flag `is_public` to the request object

    requirements:
        add middleware 'users.mixins.CustomLoginRequiredMixin' to MIDDLEWARE in settings.py

    usage:
        @public_path
        def my_view(request):
            # Your view logic here
            return render(request, 'my_template.html')
          
    """
    view_func.is_public = True
    return view_func
