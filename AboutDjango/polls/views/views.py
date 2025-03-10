from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse

from users.decorators import public_path

from ..models import Choice, Question, ImageCF

# Create your views here.
@public_path
def index(request):
    return render(request, 'index.html', {})

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, "polls/details.html", {"question": question, "error_message": "You didn't select a choice." })
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

class ListUploadView(generic.ListView):
    template_name = "polls/list_upload.html"
    context_object_name = "list_upload"

    def get_queryset(self):
        return ImageCF.objects.all()

def IndexUploadView(request):
    return render(request, "polls/index_upload.html")

def upload(request):
    if request.method == "POST":
        file = request.FILES["file"]
        image = ImageCF.objects.create(name=file.name, image=file)

    return HttpResponseRedirect(reverse("polls:listupload"))

def success(request):
    return HttpResponse
