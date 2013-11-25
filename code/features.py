import MySQLdb as mdb
import time
from pygithub3 import Github

con = mdb.connect('', '', '', '')
cur = con.cursor(mdb.cursors.DictCursor)

gh = Github(login='', password='')

cur.execute("SELECT * FROM first_pull_requests")

pull_requests = cur.fetchall()

for pr in pull_requests:
    merged = 0 if pr["merged_at"] is None else 1
    cur.execute("SELECT COUNT(*) FROM pr_comments WHERE user_login = '%s' AND created_at < '%s'" % (pr["submitted_by_name"], pr["submitted_on"].strftime('%Y-%m-%d %H:%M:%S')))
    user_activity = cur.fetchone()["COUNT(*)"]
    pr_id = pr["id"]
    repos_watch_counts = [repo.watchers for repo in gh.repos.list(user=pr["submitted_by_name"],type="owner").all() if repo.created_at < pr["submitted_on"]]
    reputation = sum(repos_watch_counts)
    cur.execute("SELECT COUNT(*) FROM pr_comments WHERE pr_id = %s" % pr["id"])
    number_comments = cur.fetchone()["COUNT(*)"]
    sql = "INSERT INTO feature_set (merged, user_activity, reputation, number_comments,  pr_id) VALUES (%s, %s, %s, %s)" % (merged, user_activity, reputation, number_comments, pr_id)
    cur.execute(sql)
    con.commit()
