from rest_framework import viewsets
from .models import User, Program, Approver, Request, Member, MemberType
from .serializers import UserSerializer, ProgramSerializer, ApproverSerializer, RequestSerializer, MemberSerializer, MemberTypeSerializer
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .forms import AddMemberForm, EditMemberForm
from django.views.generic.list import ListView



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

class ApproverViewSet(viewsets.ModelViewSet):
    queryset = Approver.objects.all()
    serializer_class = ApproverSerializer

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    #permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        program_id = request.data.get("program")

        # Check if the user is a member of the program
        is_member = Member.objects.filter(user=user, program__id=program_id).exists()

        if is_member:
            return super().create(request, *args, **kwargs)
        else:
            return Response({"detail": "User is not a member of the program"}, status=status.HTTP_403_FORBIDDEN)


class MemberTypeViewSet(viewsets.ModelViewSet):
    queryset = MemberType.objects.all()
    serializer_class = MemberTypeSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    next_page = 'home'

def program_list(request):
    programs = Program.objects.all()
    return render(request, 'program_list.html', {'programs': programs})

def program_detail(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    return render(request, 'program_detail.html', {'object': program})

def add_member(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            member_type = form.cleaned_data['member_type']

            # Check if the user is already a member of the program
            existing_member = Member.objects.filter(user=user, program=program).first()
            if not existing_member:
                member = Member(user=user, member_type=member_type, program=program)
                member.save()
            else:
                messages.error(request, 'The user is already a member of this program.')

            return HttpResponseRedirect(reverse_lazy('program_edit', args=[program.id]))
    return HttpResponseRedirect(reverse_lazy('program_edit', args=[program.id]))


class ProgramEdit(UpdateView):
    model = Program
    fields = ['name']
    template_name = 'program_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        members_and_forms = [
            (member, EditMemberForm(instance=member))
            for member in self.object.member_set.all()
        ]
        context['members_and_forms'] = members_and_forms
        context['add_member_form'] = AddMemberForm()
        return context

    def get_success_url(self):
        return reverse('program_detail', kwargs={'program_id': self.object.pk})
    
def edit_member(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    if request.method == 'POST':
        form = EditMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('program_edit', args=[member.program.id]))
    return HttpResponseRedirect(reverse_lazy('program_edit', args=[member.program.id]))

def remove_member(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    program_id = member.program.id
    member.delete()
    return HttpResponseRedirect(reverse_lazy('program_edit', args=[program_id]))

from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, ListView):
    model = Program
    template_name = 'dashboard.html'
    context_object_name = 'programs'

    def get_queryset(self):
        return Program.objects.filter(member__user=self.request.user).distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object_list.count() == 1:
            program = self.object_list.first()
            context['object'] = program
            context['members'] = program.member_set.all()
            context['pending_requests'] = program.request_set.filter(status='pending')
            context['approved_requests'] = program.request_set.filter(status='approved')
            context['rejected_requests'] = program.request_set.filter(status='rejected')
            context['info_required_requests'] = program.request_set.filter(status='info_required')

        return context

    
class RequestCreate(LoginRequiredMixin, CreateView):
    model = Request
    fields = ['request_type', 'program', 'description', 'attachments']
    template_name = 'request_create.html'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['program'].queryset = Program.objects.filter(member__user=self.request.user).distinct()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard')