from django.forms import ModelForm
from .models import Profile

class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['dp', 'school', 'batch', 'prog', 'about', "gender"]
        # help_texts = {
        #     'fl': 'The file must be of one of these types: pdf, odt, odp, doc, docx, ppt, pptx, jpg, png, txt',
        #     'name': '''
        #         The name describes what exactly the file contains. For example, 'Quiz 1' or 'Mid Term' or 'Slides on Decidability', etc.
        #         ''',
        #     'desc': '''
        #         The description contains any other information about the file that cannot be conveyed in the name. For example, 'Correction in Q2: inequality should be strict.' or 'These notes are from the extra class held on Diwali'
        #     '''
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)