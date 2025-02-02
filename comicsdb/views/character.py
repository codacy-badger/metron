import operator
from functools import reduce

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Prefetch, Q
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from comicsdb.forms.character import CharacterForm
from comicsdb.models import Character, Issue

PAGINATE = 28


class CharacterList(ListView):
    model = Character
    paginate_by = PAGINATE


class CharacterDetail(DetailView):
    model = Character
    queryset = Character.objects.select_related("edited_by").prefetch_related(
        Prefetch(
            "issue_set",
            queryset=Issue.objects.order_by(
                "series__sort_name", "cover_date", "number"
            ).select_related("series"),
        )
    )

    def get_context_data(self, **kwargs):
        context = super(CharacterDetail, self).get_context_data(**kwargs)
        character = self.get_object()
        qs = Character.objects.order_by("name")
        try:
            next_character = qs.filter(name__gt=character.name).first()
        except:
            next_character = None

        try:
            previous_character = qs.filter(name__lt=character.name).last()
        except:
            previous_character = None

        context["navigation"] = {
            "next_character": next_character,
            "previous_character": previous_character,
        }
        return context


class SearchCharacterList(CharacterList):
    def get_queryset(self):
        result = super(SearchCharacterList, self).get_queryset()
        query = self.request.GET.get("q")
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(
                    operator.and_,
                    (Q(name__icontains=q) | Q(alias__icontains=q) for q in query_list),
                )
            )

        return result


class CharacterCreate(LoginRequiredMixin, CreateView):
    model = Character
    form_class = CharacterForm
    template_name = "comicsdb/model_with_image_form.html"

    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        return super().form_valid(form)


class CharacterUpdate(LoginRequiredMixin, UpdateView):
    model = Character
    form_class = CharacterForm
    template_name = "comicsdb/model_with_image_form.html"

    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        return super().form_valid(form)


class CharacterDelete(PermissionRequiredMixin, DeleteView):
    model = Character
    template_name = "comicsdb/confirm_delete.html"
    permission_required = "comicsdb.delete_character"
    success_url = reverse_lazy("character:list")
