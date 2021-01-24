from django.db import models
import secrets
import uuid
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class PaymentPlans(models.Model):
    has_expiration = models.BooleanField(default=False)
    expiration_date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    contract_lenght = models.IntegerField()
    name = models.CharField(max_length=50)
    features = models.JSONField()

class Badges(models.Model):
    date_created = models.DateTimeField()
    name = models.CharField(max_length=50)
    condition = models.JSONField()

class User(AbstractBaseUser):
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_teacher = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_educator(self):
        return self.is_teacher

class CurrentUserPlan(models.Model):
    date_started = models.DateField()
    expiration_date = models.DateField()
    canceled = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    date_canceled = models.DateField()
    renew_date = models.DateField()
    owner = models.ForeignKey(User, verbose_name=("Current User Plan"), on_delete=models.CASCADE,related_name='plan_owner')
    payment_plan = models.ForeignKey(PaymentPlans, verbose_name=("Payment Plan Selected"), on_delete=models.PROTECT,related_name='plan_choosed')

class UserAuth(models.Model):
    one_time_code = models.CharField(max_length=6)
    expiration = models.DurationField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_auth')

class UserInfo(models.Model):
    YEAR_LEVEL = [('1', 'First Year'),
                  ('2', 'Second Year'), ('3', 'Third Year'),
                  ('4', 'Fourth Year'), ('5', 'Fift Year'), ('0', 'Graduated')]
    
    year_level = models.CharField(max_length=1, choices=YEAR_LEVEL)
    course = models.CharField(max_length=50, null=True)
    section = models.CharField(max_length=20, null=True)
    student_id = models.CharField(max_length=10, null=True)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    profile_image = models.CharField(max_length=250, null=True)
    background_image = models.CharField(max_length=250, null=True)
    read_me = models.CharField(max_length=250, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_info')
    badges = models.ManyToManyField(Badges, verbose_name=("User Badges"))

class Code(models.Model):
    code = models.CharField(verbose_name=("User Code"), max_length=50, unique=True, default=uuid.uuid4)
    revoked = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    user = models.ForeignKey(User, verbose_name=("User Unique Code"), on_delete=models.PROTECT, related_name='user_code')
    

#   ORG MODELS

class OrgApplication(models.Model):
    date_created = models.DateField()
    flagged = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    decline_reason = models.CharField(max_length=50)
    date_accepted = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_application')


class Org(models.Model):
    name = models.CharField(verbose_name=("Organization Name"), max_length=50)
    date_created = models.DateField()
    description = models.CharField(max_length=50)
    logo = models.CharField(max_length=50)
    background_image = models.CharField(max_length=50)
    verified = models.BooleanField(default=False)
    readme = models.CharField(max_length=50, null=True)
    contact_number = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    official = models.BooleanField(default=False)
    password = models.CharField(verbose_name=("Organization Password"), max_length=50)
    member_limit = models.IntegerField()
    restricted = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    restriction_type = models.IntegerField()
    owner = models.ForeignKey(User, verbose_name=("Organization Owner"), on_delete=models.PROTECT, related_name='org_owner')
    members = models.ManyToManyField(User, verbose_name=("Organization Member"))
    user_org_application = models.ManyToManyField(OrgApplication)

class UserOrg(models.Model):
    create_restricted = models.BooleanField(default=True)
    create_blocked = models.BooleanField(default=False)
    org_max_count = models.IntegerField(default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_org_control')
    org = models.ManyToManyField(Org, verbose_name=("User Created Organization"))


#VOTING SYSTEM
class Votes(models.Model):
    date_voted = models.DateTimeField()
    validated = models.BooleanField(default=False)
    ipv4_address = models.GenericIPAddressField(protocol="IPv4", unpack_ipv4=False)
    ipv6_address = models.GenericIPAddressField(protocol="IPv6")
    owner = models.ForeignKey(User, verbose_name=("VOTER"), on_delete=models.DO_NOTHING, related_name='votes_owner')


class PollCandidate(models.Model):
    position = models.CharField(max_length=50)
    partylist = models.CharField(max_length=50)
    is_disqualified = models.BooleanField(default=False)
    is_winner = models.BooleanField(default=False)
    date_created = models.DateTimeField()
    user = models.ForeignKey(User, verbose_name=('Candidate'), on_delete=models.PROTECT, related_name='poll_user_candidate')
    votes = models.ManyToManyField(Votes, verbose_name=("Candidate Votes"))


class MainPoll(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    date_created = models.DateTimeField()
    is_open = models.BooleanField(default=False)
    date_open = models.DateTimeField()
    is_stopped = models.BooleanField(default=False)
    date_close = models.DateTimeField()
    finished = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    notes = models.CharField(max_length=100)
    conditions = models.JSONField()
    owner = models.ForeignKey(User, verbose_name=("Who created the poll"), on_delete=models.PROTECT, related_name='poll_creator')
    org = models.ForeignKey(Org, verbose_name=("Poll Location"), on_delete=models.PROTECT, related_name='org_poll_owner')
    candidates = models.ManyToManyField(PollCandidate)


#Attendance System
class Attendance(models.Model):
    date = models.DateField()
    time = models.TimeField()
    ipv4_address = models.GenericIPAddressField(protocol="IPv4", unpack_ipv4=False)
    ipv6_address = models.GenericIPAddressField(protocol="IPv6")
    owner = models.ForeignKey(User, verbose_name=("Attendance Owner"), on_delete=models.DO_NOTHING, related_name='attendance_user_owner')

class Event(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    ended = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    started = models.BooleanField(default=False)
    description = models.CharField(max_length=250)
    org = models.ForeignKey(Org, verbose_name=("Event Owner"), on_delete=models.CASCADE, related_name='event_org_owner')
    event_attendance = models.ManyToManyField(Attendance)

#Forums Models

class Reply(models.Model):
    content = models.TextField()
    date_replied = models.DateTimeField()
    hearts = models.IntegerField()
    user = models.ForeignKey(User, related_name='reply_owner', on_delete=models.CASCADE)
    reply_replies = models.ForeignKey('self', related_name='reply_of_reply', on_delete=models.CASCADE)


class Post(models.Model):
    admin_only = models.BooleanField(default=False)
    date_posted = models.DateTimeField()
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)
    hearts = models.IntegerField()
    views = models.IntegerField()
    is_private = models.BooleanField(default=False)
    user = models.ForeignKey(User, related_name='post_owner', on_delete=models.CASCADE)
    org = models.ForeignKey(Org, related_name='post_owner', on_delete=models.CASCADE)
    replies = models.ManyToManyField(Reply)


