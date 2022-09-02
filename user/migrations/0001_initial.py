# Generated by Django 4.1 on 2022-09-02 02:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        max_length=12, unique=True, verbose_name="사용자 아이디"
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="비밀번호")),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("male", "남성"),
                            ("female", "여성"),
                            ("undefined", "미선택"),
                        ],
                        default="undefined",
                        max_length=20,
                        verbose_name="성별",
                    ),
                ),
                ("age", models.IntegerField(default=0, verbose_name="나이")),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        max_length=13,
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$"
                            )
                        ],
                        verbose_name="폰 번호",
                    ),
                ),
                (
                    "joined_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="가입일"),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="UserType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        choices=[("manager", "운영자"), ("general", "일반 사용자")],
                        max_length=100,
                        verbose_name="유저 유형",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "login_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="로그인"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="user_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="user.usertype",
            ),
        ),
    ]
