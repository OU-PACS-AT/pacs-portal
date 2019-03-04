from nucleus.auth import UserCredentials
from nucleus import settings

class CurrentUserMixin(object):
    
    
    def get_context_data(self, **kwargs):
        auth = UserCredentials()
        context = {}
        context =  super(CurrentUserMixin, self).get_context_data(**kwargs)
        context['user_full_name'] = auth.get_FirstName() + " " + auth.get_LastName()
        context['user_ounetid'] = auth.get_OUNetID()
        context['user_email'] = auth.get_Email()
        context['user_is_staff'] = auth.is_staff()
        context['user_is_faculty'] = auth.is_faculty()
        context['user_is_student'] = auth.is_student()
        context['user_is_admin'] = auth.is_admin()
        context['server_type'] = settings.SERVER_TYPE
        return context