# gitribution - Contribution Evaluating Framework Based On Git Log Data
This is the final project of undergraduate study of me, evaluating the contributions of an open-source project based on git log data with the help of graph-based tools.

## Data Obtaining
The data source of our framework is Git(https://git-scm.com/doc). So far we just use the log data of Git, which means there is not any privacy-accessible problems. So it's a general tool with a good compatibility on any devices and for any users.

Enter your project and type to get the first data file `commit-parent.csv`

`git log --all --pretty=format:"%H,%P,%ad"`

And then get the next log file `commit-stat.txt` by typing

`git log --all --stat`

## Graph Construction

## Weight Propagation

## Results