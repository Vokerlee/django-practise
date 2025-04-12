from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .models import TechnicalIndicator
import random

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
    total_questions = 10

    if request.method == "POST":
        # Process quiz answers
        score = 0
        answers = {}
        correct_answers = request.session.get('quiz_correct_answers', {})

        for i in range(1, total_questions + 1):
            question_key = f'question_{i}'
            user_answer = request.POST.get(question_key)
            correct_answer = correct_answers.get(question_key)
            answers[question_key] = {
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': user_answer == correct_answer
            }
            if user_answer == correct_answer:
                score += 1

        # Store results in session for review
        request.session['quiz_results'] = {
            'score': score,
            'total': total_questions,
            'answers': answers
        }

        # Set statistics message
        if score <= 1:
            stat_message = f"{score}/{total_questions} — Проигравший!"
        elif score == 2:
            stat_message = f"{score}/{total_questions} — Не особо умён!"
        elif score == 3:
            stat_message = f"{score}/{total_questions} — Типичный парень!"
        elif score == 4:
            stat_message = f"{score}/{total_questions} — Неплохо!"
        elif score == 5:
            stat_message = f"{score}/{total_questions} — Средний результат!"
        elif score == 6:
            stat_message = f"{score}/{total_questions} — Хороший результат!"
        elif score == 7:
            stat_message = f"{score}/{total_questions} — Отлично!"
        elif score == 8:
            stat_message = f"{score}/{total_questions} — Великолепно!"
        elif score == 9:
            stat_message = f"{score}/{total_questions} — Почти гений!"
        else:
            stat_message = f"{score}/{total_questions} — Гений технического анализа!"

        messages.success(request, stat_message)
        return redirect('quiz')

    # Generate quiz questions
    indicators = list(TechnicalIndicator.objects.all())
    if len(indicators) < total_questions:
        messages.error(request, f"Недостаточно индикаторов для квиза. Нужно минимум {total_questions}.")
        return render(request, "quiz.html", {'indicators': indicators})

    random.shuffle(indicators)
    questions = []
    correct_answers = {}

    question_types = [
        ("Как называется индикатор с описанием: '{}'", 'description', 'name'),
        ("Какая формула у индикатора '{}'", 'name', 'formula'),
        ("Что рекомендуется для индикатора '{}'", 'name', 'recommendation'),
        ("Какое описание у индикатора '{}'", 'name', 'description'),
    ]

    for i, indicator in enumerate(indicators[:total_questions], 1):
        q_type = random.choice(question_types)
        question_text, question_field, answer_field = q_type
        question = question_text.format(getattr(indicator, question_field)[:100])

        # Generate answer options
        correct_answer = getattr(indicator, answer_field)
        other_indicators = [ind for ind in indicators if ind != indicator]
        wrong_answers = [getattr(ind, answer_field) for ind in random.sample(other_indicators, min(4, len(other_indicators)))]
        if len(wrong_answers) < 4:
            wrong_answers.extend(["Вариант заглушка"] * (4 - len(wrong_answers)))
        answers = wrong_answers[:4]
        answers.append(correct_answer)
        random.shuffle(answers)

        questions.append({
            'id': i,
            'text': question,
            'answers': answers,
            'name': f'question_{i}'
        })
        correct_answers[f'question_{i}'] = correct_answer

    # Store correct answers in session
    request.session['quiz_correct_answers'] = correct_answers
    request.session.modified = True

    return render(request, "quiz.html", {
        'indicators': indicators,
        'questions': questions
    })
