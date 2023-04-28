from rest_framework import permissions


class IsAuthenticatedForWriting(permissions.IsAuthenticated):
    """
    Extends rest_framework IsAuthenticated permission limiting it to
    write API methods
    """

    message = 'Only authenticated users can insert a movie'

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view)
