from django import forms
from .models import Member, MemberType, User

class AddMemberForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    member_type = forms.ModelChoiceField(queryset=MemberType.objects.all())

    class Meta:
        model = Member
        fields = ['user', 'member_type']

class EditMemberForm(forms.ModelForm):
    member_type = forms.ModelChoiceField(queryset=MemberType.objects.all())

    class Meta:
        model = Member
        fields = ['member_type']