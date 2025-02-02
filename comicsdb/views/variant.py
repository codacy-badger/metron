from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic.edit import CreateView

from comicsdb.forms.variant import VariantForm
from comicsdb.models import Variant


class VariantCreate(LoginRequiredMixin, CreateView):
    model = Variant
    form_class = VariantForm
    template_name = "comicsdb/model_with_image_form.html"

    def get_success_url(self):
        slug = self.kwargs.get("slug", self.request.POST.get("slug"))

        return reverse("issue:detail", kwargs={"slug": slug})

    def get_initial(self):
        """Calculate Initial Data for the form, validate ownership of issue """
        issue_slug = self.kwargs.get("slug", self.request.POST.get("slug"))

        return {"issue_slug": issue_slug}
