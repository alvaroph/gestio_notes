from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, cycle, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            cycle=cycle,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, cycle, password=None):
        user = self.create_user(
            email=email,
            name=name,
            cycle=cycle,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    cycle = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'cycle']

    def __str__(self):
        return self.email

class Activity(models.Model):
    CYCLE_CHOICES = [
        ('DAW', 'DAW'),
        ('DAM', 'DAM'),
    ]
    MODULE_CHOICES = [
        ('DAM-M06', 'DAM-M06. Accés a dades'),
        ('DAM-M07', 'DAM-M07. Desenvolupament d’interfícies'),
        ('DAM-M08', 'DAM-M08. Progr. multimèdia i dispositius mòbils'),
        ('DAM-M09', 'DAM-M09. Programació de serveis i processos'),
        ('DAM-M10', 'DAM-M10. Sistemes de Gestió Empresarial'),
        ('DAM-M13', 'DAM-M13. Projecte'),
        ('DAW-M06', 'DAW-M06. Desenvolupament web en entorn client'),
        ('DAW-M07', 'DAW-M07. Desenvolupament web d\'entorn servidor'),
        ('DAW-M08', 'DAW-M08. Desplegament d’aplicacions web'),
        ('DAW-M09', 'DAW-M09. Disseny d’interfícies web'),
        ('DAW-M12', 'DAW-M12. Projecte'),
    ]

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    cycle = models.CharField(max_length=3, choices=CYCLE_CHOICES)
    module = models.CharField(max_length=50, choices=MODULE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Grade(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    grade = models.IntegerField()
    screenshot = models.ImageField(upload_to='screenshots/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.activity.code} - {self.grade}"
