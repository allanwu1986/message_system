I decided to used the Django web framework to write this application. The reason
for this is mainly convenience, Django has a data model that's better than the
relational model of MySQL, in addition it has facilities for creating users and
groups, sessions and authentication which makes the whole process of development
much easier. To create users and groups I used the Django admin interface. Users
can be assigned to one or more groups, and the message sending mechanism uses
these users and groups as a basis of its sending mechanism.

How to use the website:

To create users and groups, go to http(s)://www.mysite.com/admin/ to access the
Django admin interface. The homepage of the website is
http(s)://www.mysite.com/login/ which logs you in as a user created with the
admin tool.

After logging in, you can view your message clicking on messages in your Inbox.
To delete a message or mark a message, you select the appropriate checkbox and
press the "Update" button. Messages are also automatically marked as read after
they are read. To send a message, click on the "Send a message" button at the
bottom, a new page will load. Select which type of message, single user, group
or broadcast. Single user will send a message to a single user, but if you
provide a list of usernames separated by commas (no spaces in between) you can
send messages to multiple users. The same applies to group messages.
Broadcasting sends messages to all users. If sending messages is successful, a
message will appear at the bottom telling how many user it is attempting to
send the message to.

The Data model:

The data model for this app is in messages/models.py. Let's take a look at it.

from django.db import models
from django.contrib.auth.models import User

class CachedMessage(models.Model):
    writer = models.ForeignKey(User)
    message = models.CharField(max_length=1024)

class UserMessage(models.Model):
    read = models.BooleanField(default=False)
    message = models.IntegerField()

class Inbox(models.Model):
    owner = models.ForeignKey(User,unique=True)
    messages = models.ManyToManyField(UserMessage)

For those not familiar with Django model layer, basically every user has an
Inbox that contains zero or more UserMessage(s). A UserMessage contains a
field that keeps track of whether it has been read or not, and a field
'message' that points to a CachedMessage. The CachedMessage contains the
field 'writer' which tells you which user wrote the message and 'message'
that contains the actual message. Those familiar with Django may wonder why
the 'message' field in UserMessage is an integer instead of a ForeignKey, the
reason is that I want to keep track of all message that has been sent to the
user. Later, if the writer of a message wants to delete the message he can,
but if I used a ForeignKey the message will be deleted without a trace. Keeping
a pointer to the id field of CachedMessage ensures that a deleted message can
still be seen as deleted. Each time a message is sent to one or multiple users,
one CachedMessage is created, but a UserMessage is created in every inbox which
points to the message. One advantage of this design is that the writer can
delete the message after he or she has written it.

There are all sorts of problems with my application, including potential
security flaws because I didn't check to make sure that JavaScript isn't
injected into my application, and the interface being not exactly very refined.
One concern might be performance, because to send to each user a UserMessage
has to be created in every person's inbox. The other possible solution is to
create a separate inbox for each person, each group, and a universal inbox.
However, this would be a nightmare because it is complex, and special code
would be needed for changing group membership, deleting also becomes a problem
because you can't simply delete from a group or universal inbox (you have to
do something much more complicated), and is overall not much more
efficient because every time a person views the message he or she will still
need to download it. To help alleviate the time that might be taken to send
each message, if a message is being sent to a large number of users, you can
run it on a different thread.
