import sqlite3
from blog.models import Post, PostComment
con = sqlite3.connect("conversations.db")
cur = con.cursor()

posts = []
comments = []
for row in cur.execute("SELECT * FROM conversation"):
    comments.append(row)
    
for row in cur.execute("SELECT * FROM thread"):
    posts.append(row)


def findThread(pk):
    post = None
    for p in posts:
        if p[0] == pk:
            post = Post.objects.get(date_posted=p[1])
            break
        
    
    return post

for comment in comments[5:]:
    pk=comment[1]
    if pk==2:
        continue
    name = comment[2]
    email = comment[3]
    time = comment[4]
    comment = comment[5]
    post = findThread(pk)
    if post==None:
        continue
    
    comment = PostComment(name=name,
                          email=email,
                          date_posted=time,
                          comment=comment,
                          post=post,
                          isSubComment=False)
    comment.save()
    print("Saved 1")
                            
