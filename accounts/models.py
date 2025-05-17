from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models import JSONField



# Create your models here.



class UserManager(BaseUserManager):
    def create_user(self,username, password,mobile):

        if not username:
            raise ValueError("Please enter the Mobile number ")
        if not password:
            raise ValueError("Please enter the Password ")
        
        user = self.model(username=username)

        user.password = password
        user.username = username
        user.mobile = mobile
      
       
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password,mobile):
        
        user = self.create_user(username=username,password=password,mobile=mobile)
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    




class User(AbstractBaseUser):
    username=models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=255,null=True,blank=True)
    isd = models.CharField(max_length=10,default='91')
    mobile = models.CharField(max_length=10)

    password = models.CharField(max_length=220,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password','mobile']

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username'],
                         
                           name='unique_active_username'),

            models.UniqueConstraint(fields=['mobile'],
                           name='unique_active_mobile'),

        ]
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def save(self, *args, **kwargs):
        self.clean()
        if not self.pk:
            self.set_password(self.password)

        super().save(*args, **kwargs)
    

class Task(models.Model):
    asigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=255,unique=True)
    description = models.TextField(max_length=255,null=True,blank=True)
    due_date = models.DateField(max_length=10)
    STATUS = [
        ('Pending', 'Pending'),
        ('InProgress', 'InProgress'),
        ('Completed', 'Completed'),
    ] 
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    completion_report = models.TextField(max_length=10)
    start_time = models.DateTimeField(null=True, blank=True)

    workin_hours = models.CharField(max_length=220,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.title