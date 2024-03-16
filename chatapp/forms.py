from django import forms
from .models import Group





class GroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.requested_user = kwargs.pop('requested_user', None)
        super(GroupForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Group
        exclude = ['timestamp']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'members': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


    # def clean(self):
    #     cleaned_data = super().clean()
    #     members = cleaned_data.get('members')
    #     if members is not None and len(members) < 3:
    #         self.add_error('members', 'Minimum 3 members required')
    #     return cleaned_data



    # def clean(self):
    #     super(GroupForm, self).clean()
    #     members = self.cleaned_data.get('members')
    #     name = self.cleaned_data.get('name')
    #     if Group.objects.filter(name=name).exists():
    #         self._errors['name'] = self.error_class([
    #             'Group name already exist'])
    #     if len(members) < 2:
    #         self._errors['members'] = self.error_class([
    #             'Minimum 3 members required'])
    #     return self.cleaned_data



    def clean(self):
        super(GroupForm, self).clean()

        members = self.cleaned_data.get('members')
        name = self.cleaned_data.get('name')

        if Group.objects.filter(name=name).exists():
            self.add_error('name', 'Group name already exists')

        if len(members) < 2:
            self.add_error('members', 'Minimum 3 members required')
        return self.cleaned_data

    # def save(self, commit=True):
    #     instance = super(GroupForm, self).save(commit=False)
    #     if commit:
    #         instance.save()
    #         selected_members = self.cleaned_data.get('members', [])  # Get the selected members
    #         for member in selected_members:
    #             instance.members.add(member)  # Add each selected member to the many-to-many relationship
    #         instance.members.add(self.requested_user)  # Add the requested user
    #     return instance
    
    def save(self, commit=True):
        instance = super(GroupForm, self).save(commit=False)
        if commit:
            instance.save()
            selected_members = self.cleaned_data.get('members', [])  # Get the selected members
            selected_members_ids = list(selected_members.values_list('id', flat=True))
            selected_members_ids.append(self.requested_user.id)  # Add requested user's ID to the list
            instance.members.set(selected_members_ids)  # Set the many-to-many relationship
        return instance
