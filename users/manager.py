from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,name, email, mobile, password, **extra_fields):
        if not email or not mobile:
            raise ValueError("Email or Mobile must be set.")
        
        if not name:
            raise ValueError("name must be set.")
        
        if email:
            email = self.normalize_email(email)

        user = self.model(name=name, email=email, mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, mobile, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(name, email, mobile, password, **extra_fields)