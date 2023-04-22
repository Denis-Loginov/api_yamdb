import csv

from django.core.management import BaseCommand

from api_yamdb.settings import CSV_DATA_DIR
from users.models import User
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


class Command(BaseCommand):
    help = 'Импортирует данные из csv в базу данных'

    @staticmethod
    def import_static_from_csv():
        data = {
            User: {
                'path': CSV_DATA_DIR / 'users.csv',
                'columns': (
                    'id', 'username', 'email',
                    'role', 'bio',
                    'first_name', 'last_name'
                )
            },
            Category: {
                'path': CSV_DATA_DIR / 'category.csv',
                'columns': ('id', 'name', 'slug')
            },
            Genre: {
                'path': CSV_DATA_DIR / 'genre.csv',
                'columns': ('id', 'name', 'slug')
            }
        }

        for model, param in data.items():
            with open(param['path'], 'rt') as f:
                f.readline()
                obj_list = []
                for row in csv.reader(f):
                    obj_list.append(
                        model(**dict(zip(param['columns'], row)))
                    )
            model.objects.bulk_create(obj_list)

    @staticmethod
    def import_title_from_csv():
        with open(CSV_DATA_DIR / "titles.csv", "rt") as f:
            f.readline()
            obj_list = []
            columns = ('id', 'name', 'year')
            for row in csv.reader(f):
                obj_list.append(
                    Title(
                        category=Category.objects.get(id=row[3]),
                        **dict(zip(columns, row))
                    )
                )
            Title.objects.bulk_create(obj_list)

    @staticmethod
    def import_genre_title_from_csv():
        with open(CSV_DATA_DIR / "genre_title.csv", "rt") as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f):
                obj_list.append(
                    GenreTitle(
                        id=row[0],
                        title=Title.objects.get(id=row[1]),
                        genre=Genre.objects.get(id=row[2]),
                    )
                )
            GenreTitle.objects.bulk_create(obj_list)

    @staticmethod
    def import_reviews_from_csv():
        with open(CSV_DATA_DIR / "review.csv", "rt") as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f):
                obj_list.append(
                    Review(
                        id=row[0],
                        title=Title.objects.get(id=row[1]),
                        text=row[2],
                        author=User.objects.get(id=row[3]),
                        score=row[4],
                        pub_date=row[5],
                    ),
                )
            Review.objects.bulk_create(obj_list)

    @staticmethod
    def import_comments_from_csv():
        with open(CSV_DATA_DIR / "comments.csv", "rt") as f:
            f.readline()
            obj_list = []
            for row in csv.reader(f):
                obj_list.append(
                    Comment(
                        id=row[0],
                        review=Review.objects.get(id=row[1]),
                        text=row[2],
                        author=User.objects.get(id=row[3]),
                        pub_date=row[4],
                    ),
                )
            Comment.objects.bulk_create(obj_list)

    def handle(self, *args, **options):
        try:
            self.import_static_from_csv()
            self.import_title_from_csv()
            self.import_genre_title_from_csv()
            self.import_reviews_from_csv()
            self.import_comments_from_csv()
        except Exception as error:
            self.stdout.write(self.style.ERROR(error))
            raise error
        self.stdout.write(
            self.style.SUCCESS("CSV данные успешно добавлены в БД.")
        )
