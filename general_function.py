from datacenter.models import Mark, Schoolkid, Chastisement, Lesson, Subject, Commendation, Teacher
import random


COMMENDATION_EXAMPLES = '''
1. Молодец!
2. Отлично!
3. Хорошо!
4. Гораздо лучше, чем я ожидал!
5. Ты меня приятно удивил!
6. Великолепно!
7. Прекрасно!
8. Ты меня очень обрадовал!
9. Именно этого я давно ждал от тебя!
10. Сказано здорово – просто и ясно!
11. Ты, как всегда, точен!
12. Очень хороший ответ!
13. Талантливо!
14. Ты сегодня прыгнул выше головы!
15. Я поражен!
16. Уже существенно лучше!
17. Потрясающе!
18. Замечательно!
19. Прекрасное начало!
20. Так держать!
21. Ты на верном пути!
22. Здорово!
23. Это как раз то, что нужно!
24. Я тобой горжусь!
25. С каждым разом у тебя получается всё лучше!
26. Мы с тобой не зря поработали!
27. Я вижу, как ты стараешься!
28. Ты растешь над собой!
29. Ты многое сделал, я это вижу!
30. Теперь у тебя точно все получится!
'''


def get_schoolkid(name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.MultipleObjectsReturned as multiple_schoolkid_error:
        print("Multiple schoolkids are returned. Please, make your search more accurate")
        return
    except Schoolkid.DoesNotExist as no_schoolkid_error:
        print("No one schoolkid is returned. Please, make your search more accurate")
        return
    print("Got schoolkid:", schoolkid)
    return schoolkid



def fix_marks(schoolkid):
    schoolkid = get_schoolkid(schoolkid)
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2,3])
    mark_count = bad_marks.count()
    bad_marks.update(points=5)
    print("Fixed {0} marks".format(mark_count))


def remove_chastisements(schoolkid):
    schoolkid = get_schoolkid(schoolkid)
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisement_count = chastisements.count()
    chastisements.delete()
    print("Removed {0} chastisements".format(chastisement_count))


def _get_random_commendation():
    commendation_examples = [commendation_example.split('. ')[1]
                             for commendation_example in COMMENDATION_EXAMPLES.split('\n')]
    random_number = random.randint(0, len(commendation_examples)-1)
    return commendation_examples[random_number]


def add_commendation(schoolkid, subject_title):
    commendation_text = _get_random_commendation()
    lessons = Lesson.objects.filter(group_letter=schoolkid.group_letter,
                                    year_of_study=schoolkid.year_of_study,
                                    subject__title=subject_title)
    if (not lessons):
        print("No such subject or lesson for schoolkid. Please check subject title or timetable")
        return
    lesson = lessons.order_by('-date')[0]
    Commendation.objects.create(text=commendation_text, created=lesson.date,
                                schoolkid=schoolkid, subject=lesson.subject, teacher=lesson.teacher)
    print("Added commedation '{0}' on {1}".format(
        commendation_text, lesson.date))
