from __future__ import unicode_literals
from functools import wraps
from django.conf import settings
from django.http import HttpResponseRedirect
import time


def timeout_cache(timeout, debug=False):
    """Decorator to cache the result of a function call.
    Cache expires after timeout seconds.
    timeout == -1 for permanent cache.
    """

    def decorator(func):
        if debug:
            print("-- Initializing cache for", func.__name__)
        cache = {}

        @wraps(func)
        def decorated_function(*args, **kwargs):
            if debug:
                print("-- Called function", func.__name__)
            key = (args, frozenset(kwargs.items()))
            result = None
            if key in cache:
                if debug:
                    print("-- Cache hit for", func.__name__, key)

                (cache_hit, expiry) = cache[key]
                if timeout > 0:
                    if time.time() - expiry < timeout:
                        result = cache_hit
                elif timeout == -1:
                    result = cache_hit
                elif debug:
                    print("-- Cache expired for", func.__name__, key)
            elif debug:
                print("-- Cache miss for", func.__name__, key)

            # No cache hit, or expired
            if result is None:
                result = func(*args, **kwargs)

            cache[key] = (result, time.time())
            return result

        return decorated_function

    return decorator


def require_https(view):
    """A view decorator that redirects to HTTPS if this view is requested
    over HTTP. Allows HTTP when DEBUG is on and during unit tests.

    """

    @wraps(view)
    def view_or_redirect(request, *args, **kwargs):
        if not request.is_secure():
            # Just load the view on a devserver or in the testing environment.
            if settings.DEBUG or request.META['SERVER_NAME'] == "testserver":
                return view(request, *args, **kwargs)

            else:
                # Redirect to HTTPS.
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return HttpResponseRedirect(secure_url)

        else:
            # It's HTTPS, so load the view.
            return view(request, *args, **kwargs)

    return view_or_redirect
