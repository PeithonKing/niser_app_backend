from django.shortcuts import render
from django.contrib import messages
from django.utils.safestring import mark_safe

# Create your views here.

def index(request):
    if request.user is None or not request.user.is_authenticated:
        messages.error(request, "As you are not logged in, your timetable will not be saved.")
    messages.info(request, "Unimplemented: Your timetable will anyway not be saved. We will update timetable soon.")
    messages.success(request, mark_safe("Please feel free to raise feature requests related to this at <a href='https://github.com/PeithonKing/niser_app_backend/issues'>Github Issues</a>."))
    return render(request, 'timetable/index.html')