from django.shortcuts import render
from django.views.generic import TemplateView  # OOP: Inheritance từ base view

class HomeView(TemplateView):  # SRP: Chỉ render home UI
    template_name = 'index.html'  # Render index.html với DTL

    def get_context_data(self, **kwargs):  # Clean Code: Method riêng cho context (sau này thêm data)
        context = super().get_context_data(**kwargs)
        # Ví dụ: context['new_arrivals'] = []  # Sau này từ models
        return context