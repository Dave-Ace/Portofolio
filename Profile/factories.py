import factory
from factory.django import DjangoModelFactory

from .models import User, Blog, Category, Content, Paragraph, Comment, Reply

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Faker("user_name")
    email = factory.Faker("free_email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
    
    category = factory.Faker("word")
    
class BlogFactory(DjangoModelFactory):
    class Meta:
        model = Blog
    
    author = factory.SubFactory(UserFactory)
    tag = factory.SubFactory(CategoryFactory)
    title = factory.Faker(
        "sentence",
        nb_words=6,
        variable_nb_words=True)

class ContentFactory(DjangoModelFactory):
    class Meta:
        model = Content
    
    content = factory.SubFactory(BlogFactory)

class ParagraphFactory(DjangoModelFactory):
    class Meta:
        model = Paragraph
    
    paragraph = factory.SubFactory(ContentFactory)
    block = factory.Faker(
        "sentence",
        nb_words=65,
        variable_nb_words=True)

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment
    
    blog = factory.SubFactory(BlogFactory)
    name = factory.Faker("name")
    email = factory.Faker("free_email")
    comment = factory.Faker(
        "sentence",
        nb_words=65,
        variable_nb_words=True)

class ReplyFactory(DjangoModelFactory):
    class Meta:
        model = Reply
    
    comment = factory.SubFactory(CommentFactory)
    name = factory.Faker("name")
    email = factory.Faker("free_email")
    comment = factory.Faker(
        "sentence",
        nb_words=65,
        variable_nb_words=True)




