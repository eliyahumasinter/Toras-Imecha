import sqlite3
from blog.models import Post, PostComment
con = sqlite3.connect("conversations.db")
cur = con.cursor()

posts = []
comments = []
subcomments = []
for row in cur.execute("SELECT * FROM conversation"):
    comments.append(row)
    
for row in cur.execute("SELECT * FROM thread"):
    posts.append(row)

for row in cur.execute("SELECT * FROM comment"):
    subcomments.append(row)


def findThread(pk):
    post = None
    for p in posts:
        if p[0] == pk:
            post = Post.objects.get(date_posted=p[1])
            break
    return post

def findParent(pk):
    parent = None
    parentID = None
    for comment in comments:
        if comment[0] == pk:
            parent = comment
            parentID = comment[0]
            break
    d = parent[5]
    print("parentID",parentID)
    p = PostComment.objects.get(comment=d)
    return p, parentID

for comment in subcomments[4:]:
    parentCommentID = comment[1]
    name = comment[2]
    email = comment[3]
    date_posted = comment[4]
    comment = comment[5]
    parent, parentID = findParent(parentCommentID)
    post = findThread(parentID)
    comment = PostComment(
                name=name,
                email=email,
                comment=comment,
                post=post,
                isSubComment=True,
                parent=parent,
                approved=True)
    comment.save()
    
    
