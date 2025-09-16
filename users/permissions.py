from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Here, you create a new permission class named IsOwner.
    It inherits from BasePermission, which is the base class for permissions in DRF.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
    """
    This method is called when DRF checks if the user has permission for a specific object (obj).
    It compares the user attribute of the object (obj.user) with the currently logged-in user (request.user).
    If they match, it returns True → permission is granted.
    If they don't match, it returns False → permission is denied.
    """


"""
You’re building an Online Bookstore Management System:
Each book object belongs to a user (obj.user is the owner).
Only the user who created the book should be allowed to edit or delete it.
Others shouldn’t be able to access or change it.
This permission class helps you implement that rule.
"""