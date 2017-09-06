# About PET-demo

This demo shows how to transform a simple database table to a more privacy friendly version, through a privacy enhancing
technology or PET.

The demo is written for Python, version 3.6 and up. It requires no additional packages beyond the standard installation.

The code evolves in steps, each located in the directory `src` and described below.
When run, each of these scripts will produce a database in the directory `database`, which will be created on demand.
Each script will report the content of the database in tabular form.
Queries to access the databases can be found in `queries` and should be used by some database inspection tool able to
access sqlite databases (e.g. "DB Browser for SQLite").

# The database

The database stores some contact info: name, address, email, and identification number.
Data is obtained from `src/common/contacts` and shared among the scripts of each step.
Effectively, we have the same data set in each step.

The database of each step will be created in `databases`.
Each steps ends with showing the content of its database by applying the proper retrieval technique.
Compare the output with the results of the `queries` of previous steps and examine the database by hand.

# Step 01

This script is the starting point.
It defines a simple database with one table to hold the contact info.
Adding rows of data is straight forward, as is retrieving data.

A drawback is that some data is considered privacy sensitive when associated with a person:
it is personally identifiable information or PII.

# Step 02

This script stores each additional information item in its own table.
We link the additional information to the base record by the base record's primary key (here: its row id).
Adding rows becomes slightly more work. The query to retrieve data is also slightly more complex.

Although it does not solve the PII issue, this is a necessary intermediate step.
Also, the structure of the database will be very familiar to most database administrators and software developers.

# Step 03

This scripts adds hashing to the link stored in the additional information tables.
In fact, it adds keyed-hashing (a.k.a. HMAC or [**H**ash-based **M**essage **A**uthentication **C**ode][1]) to break
the backward link running from the additional information towards the base record.

With this set-up retrieving the base record and all its additional information requires minor per-record processing,
while it becomes much more cumbersome to find out which base record belongs with which piece of additional information
and requires you know the key used to compute the HMAC.

Although it seems to provide privacy protection, one can still match all associated additional information.
From there identifying the correct base record can be much easier, in this case through the email address.

[1] https://en.wikipedia.org/wiki/Hash-based_message_authentication_code

# Step 04

This script adds per-table HMAC keys.
Now there is no way to associate the various pieces of additional information.
So even if you match an email address with the proper contact name, the address and identification remain unknown.

With this set-up retrieving additional information given a base record requires computing an HMAC for each table.
Going the other way around becomes even more of a hassle.

# Conclusion

We have demonstrated how privacy in stored data can be enhanced by splitting sensitive pieces of information from the
information about the person involved. By applying HMACs on the record links we protect direct disclosure of PII.

To restore the connection between various pieces of information additional processing steps are required.
In these steps keys are used to compute the proper HMACs.
To be effective as a protective measure these keys should be kept separate from the database, both in the running
system and in backups.

# Warning

Depending on your database management system there may be ways to circumvent the privacy enhancement provided by this
technique and restore the relation between pieces of information.
There may or may not be procedures, configurations, and/or techniques to counter such restoration.
