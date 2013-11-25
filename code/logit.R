library("RMySQL")

con <- dbConnect(MySQL(),
    user="", password="",
    dbname="", host="")
on.exit(dbDisconnect(con))

feature_set <- dbGetQuery(con, "SELECT * FROM feature_set")

mylogit <- glm(merged ~ user_activity + reputation + comments_on_pr, data=feature_set, family="binomial")

# print results of logit
summary(mylogit)
