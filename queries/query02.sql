SELECT c.name, a.address, e.email, i.identification
FROM contact c, address a, email e, identification i
WHERE a.contactid = c.rowid
AND e.contactid = c.rowid
AND i.contactid = c.rowid
