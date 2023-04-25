from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """Следит за уникальностью полей email и username,
       валидирует username"""
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.RegexField(regex=r'^[\w.@+-]', max_length=150)

    class Meta:
        model = User
        fields = (
            'email',
            'username')

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                "Имя 'me' для username запрещено."
            )
        return username


class TokenSerializer(serializers.ModelSerializer):
    """Проверяет наличие username и валидирует
       код подтверждения."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())])
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code')

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if not username and not confirmation_code:
            raise serializers.ValidationError(
                f"Пустые поля: {username}, {confirmation_code}"
            )
        return data

    def validate_username(self, username):
        if not username:
            raise serializers.ValidationError(
                'Поле username не должно быть пустым'
            )
        return username


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для кастомной модели пользователя"""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())])

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует!')

        return value

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role',)


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения профиля автором"""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор моделей комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор моделей отзывов."""
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError(
                'Больше одного отзыва на title писать нельзя'
            )
        return data
