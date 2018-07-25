This document's goal is to familiarize matching tool administrators with the right places to look to investigate problems that come up in a deployment of the matching tool. 

## General Troubleshooting Tools

Below are several general tools you can use to diagnose a variety of problems. These are referred to by many of the specific use cases further down in this document.

### Querying the Database

On installation, Postgres credentials were created and put in `webapp.env`. Some troubleshooting problems may involve looking in this database. Setting up a database query tool is outside of the scope of this tutorial, but common options are [DBeaver](https://dbeaver.io/) or [psql](https://help.ubuntu.com/community/PostgreSQL#Client_Installation) (psql can be installed directly on the server).

### Logging into a container

Occasionally you may need to gain access to a shell prompt on one of the containers. You can do so with `docker exec -it <containername> /bin/bash`.

### Docker logs

Many, many troubleshooting tasks involve looking at application logs. Docker keeps track of the logs from individual docker containers and you can view them with the `docker logs` command. Try `docker logs --help` to look at all the options available to filter the logs from a specific container. Beware: some of the containers output a lot of log messages, so you won't want to run them without filtering!

## Login Issues

### A user is unable to log in

If you have created a user (see [Updating the Tool](updating.md)) but they cannot log in, you can query the webapp's [Postgres database](troubleshooting.md#querying-the-database). The user information is kept in the `public`.`user` table (with their role memberships in the `public`.`roles_users` table). That table should have an row with their email address in it. If not, their user was not successfully created and you should [create their user](updating.md) again. If they do have a row, ensure that they are logging in with the correct email address. Otherwise there may be a password issue. Although you cannot retrieve their raw password, you may remove their `user` and `roles_users` records and create a user with a fresh password for them again. Also, if you have configured the installation to be able to reset passwords (see [Installation](install.md) step 8), they may reset their password through the login page.

### A user cannot see any upload buttons

If a user can log in but cannot see any event type buttons (e.g. HMIS service stays, jail bookings) on the upload page, it means they are not a member of any roles. You can query the webapps' [Postgres database](troubleshooting.md#querying-the-database) `public`.`roles_users` table joined to the `role` and `user` tables to see what roles they are a member of.

```sql
SELECT role.name
FROM "user"
JOIN "roles_users" ON ("user".id = "roles_users".user_id)
JOIN "role" ON ("role".id = "roles_users".role_id)
WHERE email = 'thcrockett@uchicago.edu';
```

```
name            
----------------------------
default_hmis_service_stays
default_jail_bookings
(2 rows)
```

In this example, the user `thcrockett@uchicago.edu` has access to the `default_hmis_service_stays` and `default_jail_bookings` roles, which in matching tool parlance translates to `hmis_service_stays` and `jail_bookings` event types for the jurisdiction named `default`. This user should be seeing buttons on the upload page for both of those event types.

If the user does not have entries here, you may add them, either through the [create user script](updating.md) or through directly modifying the database.

If the user *does* have entries here, refer to the [docker logs](troubleshooting.md#docker-logs) in the webapp container around when they were using the application. A possible cause of this problem is if the event types they are a part of don't match the schemas listed by the app. For the most up to date list of event types, refer to `webapp/schemas/uploader/`. The filenames in that directory (dashes replaced with underscores) are queried by the app and make up a whitelist of event types. Any event type the user is associated with that doesn't match that list will be ignored by the application.

## Upload Issues

### System failure

Although the majority of messages that users will see coming from the upload portion of the tool should be *validation* errors (user-fixable, referenced in the [Users](/users/using.md) section of the guide), occasionally they may see a message that indicates a 'System Failure'/'System Error' and they need to come to you for help. In this case, there is something that failed during the upload process in a way that the system did not expect. You should look at the [docker logs](troubleshooting.md#docker-logs) for both the webapp and webapp_worker containers that cover the period that the user was using the tool. If there's a lot of output, you can filter to 'ERROR' messages (e.g. `docker logs webapp | grep ERROR`), though often the messages surrounding an error message will give helpful context.


## Matching Issues

