from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import TaskForm
from .models import Task

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đăng ký thành công! Hãy đăng nhập.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f'Chào mừng {user.username}!')
                next_url = request.GET.get('next') or request.POST.get('next')
                if next_url and url_has_allowed_host_and_scheme(
                        next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'Bạn đã đăng xuất.')
    return redirect('task_list')

@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)

    status = request.GET.get('status')
    if status == 'done':
        tasks = tasks.filter(is_completed=True)
    elif status == 'pending':
        tasks = tasks.filter(is_completed=False)

    tasks = tasks.order_by('due_date')
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'status': status,
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(request, 'Đã thêm công việc mới.')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Thêm công việc',
    })

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.owner != request.user:
        return HttpResponseForbidden('Bạn không có quyền sửa công việc này.')

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã cập nhật công việc.')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Sửa công việc',
    })


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.owner != request.user:
        return HttpResponseForbidden('Bạn không có quyền xoá công việc này.')

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Đã xoá công việc.')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
