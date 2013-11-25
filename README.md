This repository contains scripts and materials for a final project in  CS 595:
Machine Learning and Social Media. The repository is organized as follows:

    code -- contains all scripts used for data analysis, including SQL scripts
    slides -- contains project proposal and final presentation slidedecks
    tex -- contains final report LaTeX files

Data for this project was stored in a MySQL database. It was collected using
[gh-collector](https://github.com/matthewheston/gh-collector), and the scripts
here assume that the tables from the create scripts in that repository exist.
The `code` directory contains SQL files to create the tables the Python and R
scripts used for data analysis rely on.

All of the scripts used for data manipulation need credentials for your MySQL
database and GitHub API. In all cases, these values have simply been removed
from the scripts and replaced with emptry strings. There is no central
configuration file where these are stored. In order to run the scripts, you will
need to manually add this information to them.

Some of these scripts use the GitHub API in building the feature set that will
be used by the data analysis scripts. Generally, these scripts work by reading
from the table of pull requests and making GitHub API calls to retrieve more
information about the pull requests. There are limitations to running these
scripts that one should keep in mind. In their current state, they attempt to
read *all* of the records from the pull requests table. The GitHub API has a
rate limit of 5000 requests per hour for an authenticated user. If you have more
than 5000 pull requests, you'll hit this limit. In practice, this was dealt with
by modifying the the SELECT statement in those scripts to do batches of 5000 and
running the script several times. There is likely a more eloquent way of doing
this than manually updating the script and running it every hour.

To run the analyses shown in the report, the process is:

1. Set up gh-collector database tables and run data collection scripts in that
   repository (i.e., `gh-collector pull_requests --owner=rails --repo=rails --comments
   --verbose`)
2. Run SQL scripts in this repository.
3. Run `features.py` to populate the feature_set table.
4. Use `skl.py` to run classifier experiments. Run `logit.R` for logistic
   regression.
5. `include_commits_and_changes.py` is provided to update the feature set to
   include the commits and changes variables that were used in later
   experiments.

Dependencies for different parts of this project include:

- LaTeX
  - graphicx
  - ntheorem
- Python
  - MySQLdb
  - sklearn (which has its own dependencies including numpy and scipy)
  - pygithub3
- R
  - RMySQL
