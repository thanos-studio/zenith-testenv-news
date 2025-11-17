from django.db import migrations


PRESS_NAMES = [
    "아침미디어",
    "유찬일보",
    "Poop in bedchan",
    "아침조선",
    "매일아침",
]


def seed_presses(apps, schema_editor):
    Press = apps.get_model("Main", "Press")
    for name in PRESS_NAMES:
        Press.objects.get_or_create(name=name)


def remove_seeded_presses(apps, schema_editor):
    Press = apps.get_model("Main", "Press")
    Press.objects.filter(name__in=PRESS_NAMES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("Main", "0003_press_subscribers"),
    ]

    operations = [
        migrations.RunPython(seed_presses, remove_seeded_presses),
    ]
