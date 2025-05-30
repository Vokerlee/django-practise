import random

from django.shortcuts import render, redirect
from django.contrib import messages
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

        if not all([name, description, formula, recommendation]):
            messages.error(request, "Все поля обязательны для заполнения.")
            return redirect('tech_indicators')

        if 'add_indicator' in request.POST:
            try:
                TechnicalIndicator.objects.create(
                    name=name,
                    description=description,
                    formula=formula,
                    recommendation=recommendation
                )
                messages.success(request, f"Индикатор '{name}' успешно добавлен!")
            except Exception as e:
                messages.error(request, f"Ошибка при добавлении индикатора: {str(e)}")
        elif 'edit_indicator' in request.POST:
            indicator_id = request.POST.get('indicator_id')
            if not indicator_id:
                messages.error(request, "ID индикатора не указан.")
                return redirect('tech_indicators')
            try:
                indicator = TechnicalIndicator.objects.get(id=indicator_id)
                indicator.name = name
                indicator.description = description
                indicator.formula = formula
                indicator.recommendation = recommendation
                indicator.save()
                messages.success(request, f"Индикатор '{name}' успешно обновлен!")
            except TechnicalIndicator.DoesNotExist:
                messages.error(request, "Индикатор не найден.")
            except Exception as e:
                messages.error(request, f"Ошибка при обновлении индикатора: {str(e)}")
        else:
            messages.error(request, "Неверное действие.")

        return redirect('tech_indicators')

    # Render the page with the list of indicators
    return render(request, "tech_indicators.html", {"indicators": indicators})

def delete_indicator(request, indicator_id):
    try:
        indicator = TechnicalIndicator.objects.get(id=indicator_id)
        name = indicator.name
        indicator.delete()
        messages.success(request, f"Индикатор '{name}' успешно удален!")
    except TechnicalIndicator.DoesNotExist:
        messages.error(request, "Индикатор не найден.")

    return redirect('tech_indicators')

def quiz(request):
    total_questions = 10

    if request.method == "POST":
        # Process quiz answers
        score = 0
        answers = {}
        correct_answers = request.session.get('quiz_correct_answers', {})
        questions = request.session.get('quiz_questions', [])

        for i in range(1, total_questions + 1):
            question_key = f'question_{i}'
            user_answer_index = request.POST.get(question_key)
            correct_answer = correct_answers.get(question_key)
            question_data = questions[i - 1] if i <= len(questions) else {}
            question_answers = question_data.get('answers', [])

            # Convert index to answer text, handle None
            user_answer = None
            if user_answer_index is not None and user_answer_index.isdigit():
                idx = int(user_answer_index)
                if 0 <= idx < len(question_answers):
                    user_answer = question_answers[idx]

            is_correct = user_answer == correct_answer
            answers[question_key] = {
                'user_answer_index': user_answer_index,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'question_text': question_data.get('text', ''),
                'question_answers': question_answers
            }

            if is_correct:
                score += 1

        # Store results in session for review
        request.session['quiz_results'] = {
            'score': score,
            'total': total_questions,
            'answers': answers
        }

        # Score-to-message mapping
        score_messages = {
            0: "Проигравший!",
            1: "Проигравший!",
            2: "Не особо умён!",
            3: "Типичный парень!",
            4: "Неплохо!",
            5: "Средний результат!",
            6: "Хороший результат!",
            7: "Отлично!",
            8: "Великолепно!",
            9: "Почти гений!",
            10: "Гений технического анализа!"
        }

        score_message = score_messages.get(score, 'Гений технического анализа!')
        stat_message = f"{score}/{total_questions} — {score_message}"

        messages.success(request, stat_message)
        return redirect('quiz')

    # Generate quiz questions
    indicators = list(TechnicalIndicator.objects.all())
    if len(indicators) < total_questions:
        messages.error(request,
            f"Недостаточно индикаторов для квиза. Нужно минимум {total_questions}.")
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
        wrong_answers = [getattr(ind, answer_field) for ind in
            random.sample(other_indicators, min(4, len(other_indicators)))]
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
    request.session['quiz_questions'] = questions
    request.session.modified = True

    return render(request, "quiz.html", {
        'indicators': indicators,
        'questions': questions
    })
