from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Custom User Manager for Petitioner
class PetitionerManager(BaseUserManager):
    def create_user(self, email, full_name, date_of_birth, password=None, bio_id=None):
        if not email:
            raise ValueError("Email is required")
        if not bio_id:
            raise ValueError("BioID is required")
        
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            date_of_birth=date_of_birth,
            bio_id=bio_id
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, date_of_birth, password=None, bio_id=None):
        user = self.create_user(email, full_name, date_of_birth, password, bio_id)
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User Model for Petitioner
class Petitioner(AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    bio_id = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = PetitionerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'date_of_birth', 'bio_id']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

# Petition Model
class Petition(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    petitioner = models.ForeignKey(Petitioner, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, 
        choices=[('open', 'Open'), ('closed', 'Closed')], 
        default='open'
    )
    signatures = models.IntegerField(default=0)
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

# Signature Model
class Signature(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    petitioner = models.ForeignKey(Petitioner, on_delete=models.CASCADE)

    def __str__(self):
        return f"Signature by {self.petitioner.email} for {self.petition.title}"

# Item Model (from your existing setup)
class Item(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.name
    
    