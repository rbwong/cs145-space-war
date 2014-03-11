Task List:
------------
+ Protocol
    + Headers
    + Parse message
    + Commands

+ Game
    + Graphics

+ Formats
    + SETUSERNAME <username>
    + SETSTATUS <status>
    + LISTUSERS
    + SAY <msg>
    + PM <user_id> <msg>

+ Notes

frontend commands
SETUSERNAME <username>
SETSTATUS <status>
SAY <msg>
PM <username> <msg>


backend commands
GET <attribute>
SET <attribute> <new_value>
QUIT

---QUIT sequence---
1. Client sends QUIT
2. Server sends quit_key + "\Q"
3. Client sends quit_key + "\Q3"
4. Client exits
5. Server kills thread, closes connection, deletes client from dictionary