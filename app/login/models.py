from flask_login import AnonymousUserMixin


class AnonymousUser(AnonymousUserMixin):

    @staticmethod
    def has_role(_):
        """
        No Roles for anonymous users.
        """
        return False
