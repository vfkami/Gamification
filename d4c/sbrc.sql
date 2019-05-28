CREATE TABLE `EventLogs` (
	`Name` TEXT NOT NULL,
	`Institution` TEXT NOT NULL,
	`state` TEXT NOT NULL,
	`session` TEXT NOT NULL,
	`participation` TEXT NOT NULL,
	`points`TEXT NOT NULL,
	`lastScore` TEXT NOT NULL,
	`updated_at` TEXT NOT NULL
);


(%(Name)s, %(Institution)s, %(state)s, %(session)s, %(participation)s, %(lastScore)i, %(updated_at)s)

CREATE TABLE `EventLogs` 
{
	'Name': 
	'Institution' : ,
	'state' : ,
	'session' : ,
	'participation' : ,
	'lastScore' : ,
	'updated_at' :
}
);
