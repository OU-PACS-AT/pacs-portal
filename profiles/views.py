from django.contrib import messages
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy

from toolkit.views import CCEFormView, CCEUpdateView, CCETemplateView
from profiles.forms import ProfileCreateForm, SecondaryEmailChangeForm



class RegistrationView(CCEFormView):
    form_class = ProfileCreateForm
    page_title = 'Register for College of Liberal Studies'
    sidebar_group = ['registration']
    success_message = 'You have successfully registered for College of Liberal Studies'
    template_name = 'form.html'

    def form_valid(self, form):
        """
        Create user, send activation email and log them in.
        """
        try:
            user = form.create_user()
        except IntegrityError:
            messages.warning(self.request, "That username is already in use. "
                                           "Please try another.")
            return self.form_invalid(form)
        else:
            return HttpResponseRedirect(reverse('login'))

    def get_success_url(self):
        return reverse('home')

# class SecondaryEmailChange(CCEUpdateView):
#     sidebar_group = ['profiles', 'secondary_email_change']
#     template_name = 'secondary_email_change.html'
#     page_title = 'Update Secondary Email'
#     model = User
#     fields = ['email']
#     #success_url = reverse_lazy('secondary_email_change')
#     
#     #def get_context_data(self, *args, **kwargs):
#     #    context = super(SecondaryEmailChange,self).get_context_data(*args, **kwargs)
#     #    context['test'] = self.request.user
#     #    return context
#     
#     #messages.success(self.request,"Email Updated Successfully! 2")
#     #form_class = SecondaryEmailChangeForm#(data=request.POST, instance=request.user)
#     success_message = "Email Updated Successfully"
#     def get_object(self):
#         return self.request.user
    
class SecondaryEmailChange(SuccessMessageMixin, UpdateView):
    sidebar_group = ['profiles', 'secondary_email_change']
    template_name = 'secondary_email_change.html'
    page_title = 'Update Secondary Email'
    model = User
    fields = ['email']
    success_url = reverse_lazy('secondary_email_change')
     
    #def get_context_data(self, *args, **kwargs):
    #    context = super(SecondaryEmailChange,self).get_context_data(*args, **kwargs)
    #    context['test'] = self.request.user
    #    return context
     
    #messages.success(self.request,"Email Updated Successfully! 2")
    #form_class = SecondaryEmailChangeForm#(data=request.POST, instance=request.user)
    success_message = "Email Updated Successfully"
    def get_object(self):
        return self.request.user