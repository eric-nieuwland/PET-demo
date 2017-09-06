SELECT c.name, a.address, e.email, i.identification
FROM  contact c, address a, email e, identification i
WHERE a.contactid = e.contactid
AND a.contactid = i.contactid
