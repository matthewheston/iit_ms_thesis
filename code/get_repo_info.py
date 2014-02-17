import MySQLdb as mdb
import sh

con = mdb.connect('', '', '', '')
cur = con.cursor(mdb.cursors.DictCursor)
cur.execute("SELECT DISTINCT repo_name, repo_owner FROM first_pull_requests WHERE contributor_count IS NULL")

repos = cur.fetchall()

for repo in repos:
    # first, clone the repo we want
    url = 'https://github.com/%s/%s.git' % (repo['repo_owner'], repo['repo_name'])
    print "Cloning %s" % url
    sh.git("--no-pager", "clone", url, "../../mlsm_data/%s" % repo["repo_name"])
    git = sh.git.bake("--no-pager", _cwd="../../mlsm_data/%s" % repo["repo_name"])

    # then get all the pull requests associated with it
    cur.execute("SELECT * FROM first_pull_requests WHERE repo_name = '%s'" % repo["repo_name"])
    pull_requests = cur.fetchall()

    # then update each one
    for pr in pull_requests:
        print "Processing pr # %s" % pr["id"]
        commits = git("rev-list", '--before="%s"' % pr["submitted_on"],  'gh-pages')
        authors = git("log", "--format='%aN'", '--before="%s"' % pr["submitted_on"],  'gh-pages')
        commits_before_pr = len(commits.split("\n")) - 1
        authors_before_pr = len(set(authors.split("\n"))) - 1
        print authors_before_pr
        print "Updating table..."
        cur.execute("UPDATE feature_set SET repo_commits=%s, contributor_count=%s WHERE pr_id=%s", (commits_before_pr, authors_before_pr, pr["id"]))
        con.commit()
