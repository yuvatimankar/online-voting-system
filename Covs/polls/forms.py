from django import forms
from .models import Candidate, Poll

class PollForm(forms.ModelForm):

      candidate1  = forms.CharField(
                           label='First Candidate', 
                           max_length=100, 
                           min_length=3,
                           required=False, 
                           widget=forms.TextInput(attrs={'class': 'form-control'})
                           )
      candidate2  = forms.CharField(
                           label='Second Candidate', 
                           max_length=100, 
                           min_length=3,
                           required=False, 
                           widget=forms.TextInput(attrs={'class': 'form-control'})
                           )
                           
      class Meta:
          model   =  Poll
          fields  = ['title', 'candidate1', 'candidate2']
          widgets = {
              'title': forms.Textarea(attrs={"class":"form-control", "rows":1, "cols":2})
          }

class EditPollForm(forms.ModelForm):

    class Meta:
        model   = Poll
        fields  = ['title']
        widgets = {
            'title': forms.Textarea(attrs={"class":"form-control", "rows":2, "cols":2})
        }

class CandidateForm(forms.ModelForm):

    class Meta:
        model  = Candidate
        fields = ['candidate_name']