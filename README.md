# tu2

Simple CLI task time tracking. Records saved to human readable and editable plain text file.

## Start tracking time spent on task

    tu2 add <task name> [HHMM|now][-HHMM|-now] <file>


## Close open tasks

    tu2 close <file>


## Timeusage report


    tu2 report <file>

### Format

    YYYYMMDD   <hours>   <task name>
    ..
    <hours> between <first record> and <last record> @ <now>


## Show current project

    tu2 current <file>


## File structure

    YYYYMMDD HHMM	YYYYMMDD HHMM	Name