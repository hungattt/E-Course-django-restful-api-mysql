from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.name


class MyModelBase(models.Model):
    subject = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='courses/%y/%m', default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.subject


class Course(MyModelBase):
    class Meta:
        unique_together = ('subject', 'category')  # trong một danh mục k để tồn tại 2 lớp học giống nhau
        ordering = ["-id"]

    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)


class Lesson(MyModelBase):
    class Meta:
        unique_together = ('subject', 'course')  # trong một lớp học k để tồn tại 2 môn học giống nhau

    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # related_name = "lesson"
    tags = models.ManyToManyField('Tag', blank=True, null=True)


class Comment(models.Model):
    content = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    creator =models.ForeignKey(User, on_delete=models.CASCADE)  # on_delete=models.CASCADE ng dùng xóa khỏi hệ
    # thống thì tin nhắn cũng bị xóa theo
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class ActionBase(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)  # on_delete=models.CASCADE ng dùng xóa khỏi hệ

    class Meta:
        abstract = True


class Action(ActionBase):
    LIKE, HAHA, HEART = range(3)
    ACTIONS = [
        (LIKE, 'like'),
        (HAHA, 'haha'),
        (HEART, 'heart')
    ]
    type = models.PositiveSmallIntegerField(choices=ACTIONS, default=LIKE)


class Rating(ActionBase):
    rate = models.PositiveSmallIntegerField(default=0)


class LessonView(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE)
