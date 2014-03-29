library("RMySQL")

con <- dbConnect(MySQL(),
    user="root", password="mysql",
    dbname="ghdata", host="localhost")
on.exit(dbDisconnect(con))

# contains all observations
feature_set <- dbGetQuery(con, "SELECT * FROM feature_set")

# contains observations for users who submit at least
# one other pull request after their initial one
feature_set_repeaters <- dbGetQuery(con, "SELECT * FROM feature_set_repeaters")

# contains observations for users who submit at least
# five other pull requests after their initial one
feature_set_repeaters_5 <- dbGetQuery(con, "SELECT * FROM feature_set WHERE pr_id IN
(
SELECT id FROM first_pull_requests
WHERE submitted_by_id IN
(
SELECT submitted_by_id FROM
(
SELECT submitted_by_id, submitted_by_name, COUNT(submitted_by_name)  FROM pull_requests
GROUP BY submitted_by_name
HAVING COUNT(submitted_by_name)  > 5
) AS s
)
)")

# this gets counts for each user of total number of pull
# requests submitted and total number of pull_requests
# commented on.
total_pull_requests_and_commented <- dbGetQuery(con, "SELECT submitted_by_name, number_pull_requests, number_commented from
(
(SELECT submitted_by_name, COUNT(*) number_pull_requests FROM pull_requests
GROUP BY submitted_by_name) as d1
LEFT OUTER JOIN
(SELECT user_login, COUNT(DISTINCT pr_id) number_commented
FROM pr_comments prc
JOIN pull_requests pr
ON prc.pr_id = pr.id
WHERE pr.submitted_by_id != prc.user_id
GROUP BY user_login) as d2
ON d1.submitted_by_name = d2.user_login
)")
# change database nulls to 0
total_pull_requests_and_commented[is.na(total_pull_requests_and_commented)] <- 0

# this plots the number of previous pull requests a user commented on
# and the number of comments they receive on the pull request they submit.
ggplot(data=feature_set,aes(x=number_comments,y=comments_on_pr)) + geom_point(size=4,aes(shape=factor(merged))) + labs(x="User Participation", y="Attention Pull Request Receives") + labs(shape="Merged")

# this plots the number of previous pull requests a user commented on
# and the number of comments they receive on the pull request they submit
# for users that submit at least one more time after first pull request.
ggplot(data=feature_set_repeaters,aes(x=number_comments,y=comments_on_pr)) + geom_point(size=4,aes(shape=factor(merged))) + labs(x="User Participation", y="Attention Pull Request Receives") + labs(shape="Merged")

# this plots the number of previous pull requests a user commented on
# and the number of comments they receive on the pull request they submit
# for users that submit at least five more times after first pull request.
ggplot(data=feature_set_repeaters_5,aes(x=number_comments,y=comments_on_pr)) + geom_point(size=4,aes(shape=factor(merged))) + labs(x="User Participation", y="Attention Pull Request Receives") + labs(shape="Merged")

# get the correlation between total number of pull requests submitted and total
# number commented on.
cor(total_pull_requests_and_commented$number_pull_requests, total_pull_requests_and_commented$number_commented)

# get the correlation between total number of pull requests submitted and total
# number commented on.
cor.test(total_pull_requests_and_commented$number_pull_requests, total_pull_requests_and_commented$number_commented, method="spearman")
