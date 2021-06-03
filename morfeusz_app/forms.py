from django import forms
from users.models import FriendList


class CreateGroupForm(forms.Form):
    name = forms.CharField(label="Name your group")


class AddGroupMember(forms.Form):

    friend = forms.ChoiceField(choices=[])

    def __init__(self, friend):
        super(AddGroupMember, self).__init__()
        self.fields['friend'].choices = friend
