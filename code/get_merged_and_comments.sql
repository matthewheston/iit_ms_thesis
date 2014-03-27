-- this returns the comments for each pull request in our feature set and
-- whether or not it was merged

SELECT new_merged, GROUP_CONCAT(REPLACE(REPLACE(prc.body, '\n', ' '), '\r', ' ') SEPARATOR '|') AS `comments`
FROM feature_set fs
JOIN pr_comments prc
ON fs.pr_id = prc.pr_id
JOIN pull_requests pr
ON fs.pr_id = pr.id
WHERE prc.user_id != pr.submitted_by_id
GROUP BY prc.pr_id

-- then we use perl to find only ones that have more than one comment
-- perl -ne '/\|/ && print' merged_and_comments.tsv
-- and we'll use python to get rid of last comments
-- something like: [line.split("|")[0:-1].join(" ") for line in content];
