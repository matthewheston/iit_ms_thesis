import MySQLdb as mdb
import time
from pygithub3 import Github

con = mdb.connect('', '', '', '')
cur = con.cursor(mdb.cursors.DictCursor)

gh = Github(login='', password='')

cur.execute("SELECT * FROM first_pull_requests")

pull_requests = cur.fetchall()

for pr in pull_requests:
    pr_id = pr["id"]
    pr_info = gh.pull_requests.get(pr["number"], user=pr["repo_owner"], repo=pr["repo_name"])
    sql = "UPDATE feature_set SET commits=%s, changes=%s WHERE pr_id = %s" % (pr_info.commits, pr_info.additions + pr_info.deletions, pr_id)
    cur.execute(sql)
    con.commit()
