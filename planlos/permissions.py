# coding: utf-8

# berechtigungen
# ein user hat verschiedene Rollen
# ein Objekt hat verschieden Sichtweisen (show, edit, delete, copy, update)
# Jede Sichtweise kann verschiedene Permissions haben
# Eine Permission kann eine Rolle vorraussetzen
# Eine Rolle kann sein z.b. Moderator, Authenticated User, Owner, Friend

from flaskext.login import current_user


class PermissionDenied(Exception):
    pass


class UserPermission(object):
    def __init__(self, role):
        self.roles = [role]

    def require(self, f):
        def _decorated():
            for role in user.roles:
                if role in current_user.roles:
                    f()
                    return
            raise PermissionDenied()
        return _decorated


class Grant(object):
    def __init__(self, obj, role_provider, view):
        self.obj = obj
        self.role_provider = role_provider
        self.view = view

    def is_allowed(self):
        # special cases
        if 'all' in self.obj.permissions[self.view]:
            return True
        for need in self.obj.permissions[self.view] + ['admin', 'owner']:
            if need in self.role_provider.roles:
                return True
            # special needs (owner, friend, group, ...)
            if need in ['owner', 'friend']:
                try:
                    getattr(self.obj, '_need_' + str(need), self.role_provider)
                    return True
                except:
                    pass
        return False

    def __enter__(self):
        # special cases
        if 'all' in self.obj.permissions[self.view]:
            return
        for need in self.obj.permissions[self.view] + ['admin', 'owner']:
            if need in self.role_provider.roles:
                return
            # special needs (owner, friend, group, ...)
            if need in ['owner', 'friend']:
                try:
                    getattr(self.obj, '_need_' + str(need), self.role_provider)
                    return
                except:
                    pass
        # if there was no 'return' we don't have correct permissions
        raise PermissionDenied()

    def __exit__(self, type, value, traceback):
        if isinstance(value, PermissionDenied):
            abort(401)
        else:
            return True


# termine erstellen aber nicht veröffentlichen
#user_authenticated = Permission(RoleNeed('authenticated'))

# darf was?
#moderator = Permission(RoleNeed('moderator'))

# alles
#admin_permission = Permission(RoleNeed('admin'))
#admin = moderator.union(user_authenticated).union(admin_permission)



