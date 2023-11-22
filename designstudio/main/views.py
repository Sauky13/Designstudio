from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import TemplateView
from .forms import UserRegisterForm, ApplicationForm, ApplicationStatusChangeForm, CategoryForm
from .models import AdvUser, Category
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Application
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic


def index(request):
    if request.user.is_authenticated:
        completed_applications = Application.objects.filter(
            status='C', user=request.user
        ).order_by('-time_mark')[:4]

        in_progress_count = Application.objects.filter(
            status='B', user=request.user
        ).count()

        context = {
            'completed_applications': completed_applications,
            'in_progress_count': in_progress_count,
        }
    else:
        context = {}
    return render(request, 'main/index.html', context)


class LoginViewUser(LoginView):
    template_name = 'main/login.html'


class LogoutViewUser(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


@login_required
def profile(request):
    return render(request, 'main/profile.html')


class UserRegisterView(CreateView):
    model = AdvUser
    form_class = UserRegisterForm
    template_name = 'registration/register_user.html'
    success_url = reverse_lazy('main:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'


@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect('main:application_create_done')
    else:
        form = ApplicationForm()

    return render(request, 'main/application_create.html', {'form': form})


class ApplicationCreateDone(TemplateView):
    template_name = 'main/application_create_done.html'


@login_required
def view_user_applications(request):
    status_filter = request.GET.get('status_filter')

    if request.user.is_superuser:
        applications = Application.objects.all()
    else:
        applications = Application.objects.filter(user=request.user)

    if status_filter:
        applications = applications.filter(status=status_filter)

    return render(request, 'main/application_list.html', {
        'applications': applications,
        'status_filter': status_filter,
        'status_choices': Application.STATUS_CHOICES
    })




class ApplicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Application
    success_url = reverse_lazy('main:view_user_applications')
    template_name = 'main/application_confirm_delete.html'

    def test_func(self):
        application = self.get_object()
        user = self.request.user
        return user.is_superuser or application.user == user


@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    return render(request, 'main/application_detail.html', {'application': application})


@login_required
@permission_required('is_staff')
def change_application_status(request, pk):
    application = get_object_or_404(Application, pk=pk)

    if request.method == 'POST':
        form = ApplicationStatusChangeForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            return redirect('main:view_user_applications')
        else:
            return render(request, 'main/change_status.html', {'form': form, 'application': application})
    else:
        form = ApplicationStatusChangeForm(instance=application)

    return render(request, 'main/change_status.html', {'form': form, 'application': application})


class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 10


class CategoryCreate(PermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    permission_required = 'application.add_category'
    success_url = reverse_lazy('main:category')


class CategoryDelete(PermissionRequiredMixin, DeleteView):
    model = Category
    permission_required = 'application.delete_category'
    success_url = reverse_lazy('main:category')
