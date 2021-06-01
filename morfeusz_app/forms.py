from django import forms
from users.models import FriendList


class CreateGroupForm(forms.Form):
    name = forms.CharField(label="Name your group")


class AddGroupMember(forms.Form):
    # GEEKS_CHOICES = (
    #     ("1", "One"),
    #     ("2", "Two"),
    #     ("3", "Three"),
    #     ("4", "Four"),
    #     ("5", "Five"),
    # )
    friend = forms.ChoiceField(choices=[])

    def __init__(self, friend):
        super(AddGroupMember, self).__init__()
        self.fields['friend'].choices = friend
    #     my_choices = kwargs.pop('friend')
    #     super().__init__(*args, **kwargs)
    #     self.fields['friend'].choices = my_choices
