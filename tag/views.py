from dal import autocomplete
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Tag
from django.forms.models import ModelChoiceIterator, ModelMultipleChoiceField


class Autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(Tag_name__istartswith=self.q)

        return qs


def BasicDALView(request):
    js = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.js" crossorigin="anonymous"></script>
    """

    dal_media = autocomplete.Select2().media

    url = reverse_lazy('test')
    field = ModelMultipleChoiceField(Tag.objects.all())

    widget = autocomplete.ModelSelect2(
        url=url,
        attrs={"class": "selector", "data-placeholder": "과목선택"})

    widget.choices = ModelChoiceIterator(field)

    default = None
    widget_html = widget.render(Tag.__name__, default)

    html = f"<head>{js}\n{dal_media}</head><body><p>{widget_html}</p></body>"

    return HttpResponse(html)
