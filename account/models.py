from django.db import models
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser,PermissionsMixin)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _




class UserManager(BaseUserManager) :
    def create_user(self, email, nickname, password=None):
        """
        주어진 이메일,닉네임,비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            email = self.normalize_email(email),
            nickname = nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상이 사용자이므로 권한을 부여한다
        """
        user = self.create_user(
            email=email,
            password=password,
            nickname=nickname,
            # last_name=last_name,
            # first_name=first_name,
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin) :

    GENDER_CHOICE = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('not-specified', 'Not specified'),
    ) 

    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        unique=True,
    )
    nickname = models.CharField(
        verbose_name=_('Nickname'),
        max_length=30,
        unique=True
    )
    name = models.CharField(max_length=30,null=True)
    profile_image = models.ImageField(null=True)
    bio = models.TextField(null=True)
    website = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=140, null=True)
    gender = models.CharField(max_length=80, choices=GENDER_CHOICE, null=True)
    followers = models.ManyToManyField("self", blank=True, related_name='followers')
    following = models.ManyToManyField("self", blank=True, related_name='following')
    
    # first_name = models.CharField(
    #     verbose_name=_('first_name'),
    #     max_length=30,
    #     null=True
    # )
    # last_name = models.CharField(
    #     verbose_name=_('last_name'),
    #     max_length=30,
    #     null=True
    # )
    is_active = models.BooleanField(
        verbose_name=_('Date joined'),
        default=True
    )
    date_joined = models.DateTimeField(
        verbose_name=_('Date joined'),
        default=timezone.now
    )
    # 이 필드는 레거시 시스템 호환을 위해 추가할 수도 있다.
    # salt = models.CharField(
    #     verbose_name=_('Salt'),
    #     max_length=10,
    #     blank=True
    # )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname',]

    @property
    def post_count(self):
        return self.images.all().count()

    @property
    def followers_count(self):
        return self.followers.all().count()

    @property
    def following_count(self):
        return self.following.all().count()

    # @property
    # def followings_count(self):
    #     return self.following.all().count()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined',)

    def __str__(self):

        return self.nickname

    def get_full_name(self):

        return self.nickname

    def get_short_name(self):
        
        return self.nickname
    
    @property
    def is_staff(self) :
        "Is the user a member of staff?"
        return self.is_superuser

    
        
    get_full_name.short_description = _('Full name')

