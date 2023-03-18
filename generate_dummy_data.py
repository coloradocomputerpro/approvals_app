import os
import django
from django.utils import timezone
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'approval_project.settings')
django.setup()

from requests_app.models import Request, Program, Member, MemberType
from django.contrib.auth.models import User


def create_users(num_users):
    fake = Faker()
    for i in range(num_users):
        user = User.objects.create_user(
            username=fake.unique.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            password='password123',
            is_staff=fake.boolean(chance_of_getting_true=10),
            is_superuser=fake.boolean(chance_of_getting_true=5)
        )
        print(f"Created user: {user}")


def create_member_types():
    member_types = [
        {'type_name': 'Student'},
        {'type_name': 'Faculty'},
        {'type_name': 'Staff'}
    ]
    for member_type in member_types:
        MemberType.objects.create(**member_type)
        print(f"Created member type: {member_type}")


def create_programs(num_programs):
    fake = Faker()
    member_types = MemberType.objects.all()
    for i in range(num_programs):
        program = Program.objects.create(
            name=fake.unique.word(),
            description=fake.text(),
            #program_type=fake.word()
        )
        print(f"Created program: {program}")
        num_members = fake.random_int(min=1, max=10)
        members = User.objects.filter(is_staff=False, is_superuser=False).order_by('?')[:num_members]
        for member in members:
            member_type = member_types[fake.random_int(min=0, max=len(member_types) - 1)]
            Member.objects.create(
                user=member,
                program=program,
                member_type=member_type
            )
            print(f"Added {member} to {program} as a {member_type} member")

# not working, needs to be finished
def create_requests(num_requests):
    fake = Faker()
    programs = Program.objects.all()
    for i in range(num_requests):
        request = Request.objects.create(
            request_text=fake.text(),
            request_date=fake.date_time_this_month(before_now=True, after_now=False, tzinfo=timezone.utc),
            program=programs[fake.random_int(min=0, max=len(programs) - 1)]
        )
        print(f"Created request: {request}")


if __name__ == '__main__':
    create_users(20)
    create_member_types()
    create_programs(5)
    #create_requests(10)
