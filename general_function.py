from datacenter.models import Mark, Schoolkid, Chastisement, Lesson, Subject, Commendation, Teacher
import random


COMMENDATION_EXAMPLES = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!',
]


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
    random_number = random.randint(0, len(COMMENDATION_EXAMPLES)-1)
    return COMMENDATION_EXAMPLES[random_number]


def add_commendation(schoolkid, subject_title):
    commendation_text = _get_random_commendation()
    lessons = Lesson.objects.filter(group_letter=schoolkid.group_letter,
                                    year_of_study=schoolkid.year_of_study,
                                    subject__title=subject_title)
    if (not lessons):
        print("No such subject or lesson for schoolkid. Please check subject title or timetable")
        return
    lesson = lessons.order_by('-date').first()
    Commendation.objects.create(text=commendation_text, created=lesson.date,
                                schoolkid=schoolkid, subject=lesson.subject, teacher=lesson.teacher)
    print("Added commedation '{0}' on {1}".format(
        commendation_text, lesson.date))
