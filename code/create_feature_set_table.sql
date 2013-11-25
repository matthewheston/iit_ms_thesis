CREATE TABLE `feature_set` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `merged` int(1) DEFAULT NULL,
  `user_activity` int(11) DEFAULT NULL,
  `comments_on_pr` int(11) DEFAULT NULL,
  `reputation` int(11) DEFAULT NULL,
  `pr_id` int(11) unsigned NOT NULL,
  `commits` int(11) DEFAULT NULL,
  `changes` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `pr_fk` (`pr_id`),
  CONSTRAINT `pr_fk` FOREIGN KEY (`pr_id`) REFERENCES `pull_requests` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20091 DEFAULT CHARSET=utf8;
