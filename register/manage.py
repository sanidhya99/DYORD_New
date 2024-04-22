from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self,email,name,number,password=None,password2=None,**extra_fields):
        if not email:
            raise ValueError("ECN not found!")
        email=self.normalize_email(email)
        user=self.model(email=email,name=name,number=number,**extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,name,number,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        # extra_fields.setdefault('is_admin',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        return self.create_user(email,name,number,password,**extra_fields)




