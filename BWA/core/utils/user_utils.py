from MGL.middleware import get_current_user

from .command_utils import CommandeUtils


class UserUtils:

    @staticmethod
    def get_current_authenticated_user():
        try:
            user = get_current_user()
        except:
            user = None
        return user

    @staticmethod
    def get_current_authenticated_user_email():
        try:
            user = UserUtils.get_current_authenticated_user()
            return user.email
        except:
            if CommandeUtils.is_command_running():
                return CommandeUtils.get_command_name()
            return 'AnonymousUser'
