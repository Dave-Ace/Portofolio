
import random
from django.db import transaction
from django.core.management.base import BaseCommand

from Profile.models import Category, User, Blog, Comment, Reply, Content, Paragraph

from Profile.factories import (
    CategoryFactory,
    UserFactory,
    BlogFactory,
    CommentFactory,
    ReplyFactory,
    ContentFactory,
    ParagraphFactory
)
NUM_USERS = 1
BLOG_PER_CAT = 5
NUM_CAT = 10
PAR_PER_CON = 5
COM_PER_BLOG = 3
REP_PER_COM = 1

class Command(BaseCommand):
    help = "Generates test data"
    
    @transaction.atomic
    def handle(self, *args, **kwargs):
        
        self.stdout.write("Deleting old data...")
        models = [Category, Blog, User, Content, Paragraph, Comment, Reply]
        for m in models:
            if m == User:
                m.objects.filter(is_superuser=False).delete()
            else:
                m.objects.all().delete()
        
        self.stdout.write("Creating new data...")
        #Create all the users
        people = []
        for i in range(NUM_USERS):
            person = UserFactory()
            person.set_password('toluwani')
            person.is_staff = True
            person.save()
            people.append(person)
            #Crate user profile
            
        #create category
        for i in range(NUM_CAT):
            category = CategoryFactory()
            
            b_user = random.choice(people)
            #create blog for each category
            for i in range(BLOG_PER_CAT):
                blog = BlogFactory(author=b_user, tag=category)
                #create content for each blog
                content = Content.objects.get(content=blog)
                #create paragraph for each content
                for i in range(PAR_PER_CON):
                    ParagraphFactory(paragraph=content)
                    #create comment for each blog
                    for i in range(COM_PER_BLOG):
                        comment = CommentFactory(blog=blog)
                        #create reply for each comment
                        for i in range(REP_PER_COM):
                            ReplyFactory(comment=comment)



