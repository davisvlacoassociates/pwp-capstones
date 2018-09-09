
class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def __repr__(self):
        return "This user: {name}, with email{email} has read{books} books"

    def change_email(self, new_email):
        self.email = new_email
        return "This user's emil has been changed to: {email}"

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        return sum([rating for rating in self.books.values() if rating is not None]) / len(self.books)

    def get_book_read_count(self):
        return len(self.books)

    def __hash__(self):
        return hash((self.name, self.email))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def __repr__(self):
        return "Title: {book},ISBN: {isbn}"

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        return "This book's ISBN has been changed to: {isbn}"

    def add_rating(self, rating):
        try:
            if 0 <= rating <= 4:
                self.ratings.append(rating)
            else:
                return "Invalid Rating."

        except TypeError:
            "Invalid Type."

    def get_average_rating(self):
        return sum([rating for rating in self.ratings]) / len(self.ratings)

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn


class Fiction(Book):
    
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def __repr__(self):
        return "Title: {title}\n" \
               "Author: {author}\n" \
               "ISBN: {isbn}\n" \
                .format(title=self.title,
                        author=self.author,
                        isbn=self.isbn)

    def get_author(self):
        return self.author


class NonFiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def __repr__(self):
        return "Title: {title}\n" \
                "Level: {level}\n" \
                "Subject: {subject}\n" \
                "ISBN: {isbn}\n" \
                .format(title=self.title,
                        level=self.level,
                        subject=self.subject,
                        isbn=self.isbn)

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level


class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def __repr__(self):
        return "--TomeRater-{users_count}Books: {books_count}Total amount of times the books have been read: {reading_times}"
            .format(self.users,self.books,reading_times=self.get_all_users_read_count)

    @staticmethod
    def create_book(title, isbn):
        return Book(title, isbn)

    @staticmethod
    def create_novel(title, author, isbn):
        return Fiction(title, author, isbn)

    @staticmethod
    def create_non_fiction(title, subject, level, isbn):
        return NonFiction(title, subject, level, isbn)

    def add_user(self, name, email, books=None):
        if email not in self.users:
            self.users[email] = User(name, email)
            if books is not None:
                for book in books:
                    self.add_book_to_user(book, email)
        else:
            print("This user already exists.")

    def add_book_to_user(self, book, email, rating=None):
        user = self.users.get(email, "No user with email: {email}".format(email=email))

        if user:
            user.read_book(book, rating)
            book.add_rating(rating)

            self.books[book] = self.books.get(book, 0) + 1

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def get_all_users_read_count(self):
        return sum([user.get_book_read_count() for user in self.users.values()])

    def most_read_book(self):
        return max(self.books, key=self.books.get)

    def highest_rated_book(self):
        highest_rated = max(rating.get_average_rating() for rating in self.books.keys())

        return str([book for book in self.books.keys() if book.get_average_rating() == highest_rated]).strip('[]')

    def most_positive_user(self):
        highest_rated = max(rating.get_average_rating() for rating in self.users.values())

        return str([user for user in self.users.values() if user.get_average_rating() == highest_rated]).strip('[]')

    def get_n_read_books(self, number):
        if number > 0:

            for book, read in sorted(self.books.items(), key=lambda key_value: key_value[1], reverse=True)[:number]:
                    print("{book}Read: {read} times.\n".format(book=book, read=read))

            if number > len(self.books):
                print("Only printed: {count}\n"
                      "Didn't print the remaining {remaining}, because the list is not long enough."
                      .format(count=len(self.books),
                              remaining=number - len(self.books)))

        else:
            return "Entered number is below 1."

        return ""

    def get_n_prolific_readers(self, number):
        if 0 < number:
            users_sorted = {}

            for user in self.users.values():
                users_sorted[user] = user.get_book_read_count()

            users_sorted = sorted(users_sorted.items(), key=lambda key_value: key_value[1], reverse=True)[:number]

            for user, books_read_count in users_sorted:
                print("{}\n".format(user))

            if number > len(self.users):
                print("Only printed: {count}\n"
                      "Didn't print the remaining {remaining}, because the list is not long enough."
                      .format(count=len(self.users),
                              remaining=number - len(self.users)))

        else:
            return "Entered number is below 1."

        return ""

    def __eq__(self, other_tomerater):
        return self.users == other_tomerater.users and self.books == other_tomerater.books
