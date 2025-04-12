from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .models import TechnicalIndicator

def index(request):
    return render(request, "index.html")

def tech_indicators(request):
    # Fetch all technical indicators from the database
    indicators = TechnicalIndicator.objects.all()

    # Handle form submission to add a new indicator
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        formula = request.POST.get("formula")
        recommendation = request.POST.get("recommendation")

        # Basic validation
        if name and description and formula and recommendation:
            TechnicalIndicator.objects.create(
                name=name,
                description=description,
                formula=formula,
                recommendation=recommendation
            )
            messages.success(request, "Новый индикатор успешно добавлен!")
            return redirect("indicators")
        else:
            messages.error(request, "Все поля должны быть заполнены.")

    # Render the page with the list of indicators
    return render(request, "tech_indicators.html", {"indicators": indicators})

def delete_indicator(request, indicator_id):
    if request.method == "POST":
        try:
            indicator = TechnicalIndicator.objects.get(id=indicator_id)
            indicator_name = indicator.name
            indicator.delete()
            messages.success(request, f"Индикатор '{indicator_name}' успешно удален!")
            return redirect("indicators")
        except TechnicalIndicator.DoesNotExist:
            messages.error(request, "Индикатор не найден.")
            return redirect("indicators")

    return HttpResponseBadRequest("Недопустимый метод запроса.")

def quiz(request):
    return render(request, "quiz.html")
