CREATE TABLE `feature_set` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `merged` int(1) DEFAULT NULL,
  `number_comments` int(11) DEFAULT NULL,
  `comments_on_pr` int(11) DEFAULT NULL,
  `popularity` int(11) DEFAULT NULL,
  `lsm` float DEFAULT NULL,
  `pr_id` int(11) unsigned NOT NULL,
  `commits` int(11) DEFAULT NULL,
  `changes` int(11) DEFAULT NULL,
  `repo_commits` int(11) DEFAULT NULL,
  `contributor_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pr_fk` (`pr_id`),
  CONSTRAINT `pr_fk` FOREIGN KEY (`pr_id`) REFERENCES `pull_requests` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20091 DEFAULT CHARSET=utf8;