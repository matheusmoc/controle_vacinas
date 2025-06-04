from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from faker import Faker
import random
from pacientes.models import CustomUser
class Command(BaseCommand):
    help = 'Create 50 test users with random roles and names'

    def handle(self, *args, **kwargs):
        fake = Faker()
        roles = [role[0] for role in CustomUser.ROLE_CHOICES]  
        
        users_data = [
            {
                'username': f'{i+1}',
                'email': f'user{i+1}@example.com',
                'password': f'password{i+1}',
                'role': random.choice(roles),
                'first_name': fake.first_name(),
                'last_name': fake.last_name()
            }
            for i in range(50)
        ]

        users = []
        for user_data in users_data:
            user = CustomUser(
                username=user_data['username'],
                email=user_data['email'],
                password=make_password(user_data['password']),
                role=user_data['role'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
            )
            users.append(user)

        CustomUser.objects.bulk_create(users)
        self.stdout.write(self.style.SUCCESS('50 usuários de teste criados com sucesso!'))
