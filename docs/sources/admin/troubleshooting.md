This document's goal is to familiarize matching tool administrators with the right places to look to investigate problems that come up in a deployment of the matching tool. 

## Data Flow Overview

To help with general troubleshooting, it helps to gain some familiarity with how data flows through the application and different containers. Below is a step-by-step overview of data flow.

1. The user uploads a tabular dataset through the webapp UI, which is run by the `webapp` container. This data goes through the [upload_file](https://github.com/dssg/matching-tool/blob/master/webapp/webapp/apis/upload.py#L299) endpoint and is immediately saved to a temporary directory on the filesystem that is shared with the `webapp_worker` container. It tells the `webapp_worker` container to validate the file asynchronously and begins polling the asynchronous job for results.
2. The `webapp_worker` container runs the (validate_async)[https://github.com/dssg/matching-tool/blob/master/webapp/webapp/apis/upload.py#L193] function asynchronously. This saves some metadata about the upload to the `upload_log` Postgres table and runs a variety of validations on the data. It culminates in uploading the validated and transformed file to storage (S3 by default) at the (`RAW_UPLOADS_PATH`)[https://github.com/dssg/matching-tool/blob/master/webapp.env] location, and returns the validation results.
3. Assuming the file has no validation problems and the user clicks 'confirm upload', the (merge_file)[https://github.com/dssg/matching-tool/blob/master/webapp/webapp/apis/upload.py#L337] endpoint is called. This loads the stored file into the database under the path `raw_{upload_id}` and merges it with the 'master' table for the relevant jurisdiction and event type.

This 'master' table serves as both the source for the results dashboard. Data is sent from here to the matcher, and data from the matcher is synced back into it. The 'merge' consists of adding rows from the new uploaded file that do not have their primary keys (see primaryKey attribute of the relevent (schema file)[https://github.com/dssg/matching-tool/tree/master/webapp/schemas/uploader] present in the master table, and updating data in the master table with any matching rows from the upload. Placeholder matching ids (of format {event_type}_{internal_person_id}) are populated.

The 'master' table is exported to storage (at (`MERGED_UPLOADS_PATH`)[https://github.com/dssg/matching-tool/blob/master/webapp.env]) and the `matcher_worker` container is notified (via the (do_match)[https://github.com/dssg/matching-tool/blob/master/matcher/matcher/tasks.py] function) to begin matching asynchronously.
4. The `matcher_container` loads *all* master tables from storage for matching.  It loads the (matcher_config.yaml)[https://github.com/dssg/matching-tool/blob/master/matcher/matcher_config.yaml] file in the container for configuration. The internals of the matching algorithm are outside of the scope of this document, but its data output is written to storage (at (`BASE_PATH/matched`)[https://github.com/dssg/matching-tool/blob/master/webapp.env]) , and the `webapp_worker` is notified of the completed matching job.
5. The `webapp_worker` container runs the (match_finished)[https://github.com/dssg/matching-tool/blob/master/matcher/matcher/tasks.py] function to merge the matched data into the `master` table. The new data is loaded into a temporary table again and joined with the `master` table on the primary key again, this time just uploading the matched_id column with the new values from the matcher.
6. As the user queries the results dashboard, the `master` table is queried.


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

Although the majority of messages that users will see coming from the upload portion of the tool should be *validation* errors (user-fixable, referenced in the [Users](/users/using.md) section of the guide), occasionally they may see a message that indicates a 'System Failure'/'System Error' and they need to come to you for help. In this case, there is something that failed during the upload process in a way that the system did not expect. You should look at the [docker logs](troubleshooting.md#docker-logs) for both the webapp and `webapp_worker` containers that cover the period that the user was using the tool. If there's a lot of output, you can filter to 'ERROR' messages (e.g. `docker logs webapp | grep ERROR`), though often the messages surrounding an error message will give helpful context.


## Matching Issues

### Matching Failure

If a user reports that the app's timeline indicates that a matching job failed, you can look at the [docker logs](troubleshooting.md#docker-logs) for the `matcher_worker` container. Warning: The matcher outputs a **lot** of log messages, you will likely want to heavily filter the logs. For instance, just looking at the last 100 lines or so (e.g. ``docker logs matcher_worker --tail 100`` would let you see any errors that were thrown and stopped the matching job.

### Matching Oddities
Sometimes, the matching process may complete but the results look weird. Often this may show itself in the form of matching results being far lower than expected, and is corroborated by placeholder match ids (the placeholder format is `{event_type}_{person_id}`, e.g. `hmis_service_stays_123897124` showing up in the webapp results dashboard. This means that the database table that the webapp uses to populate the dashboard did not receive all of the rows of matching results it expected to receive. The reasons for this can be divided into two possibilities: Either the matcher's results (that are saved to S3) were incorrect, or they were loaded incorrectly. To find out which, compare the length of the matcher's results to the length of the corresponding database table. The matcher's results are located under the `BASE_PATH` (defined webapp.env)/matched key/file. The database [table to query](troubleshooting.md#querying-the-database) is `{jurisdiction}_{event_type}_master`.

- If the matcher results are shorter, then a problem happened with the matching service or prior to that. You can perform the same type of length check on the matcher's input at `BASE_PATH/merged` to ensure that the matcher received the correct length dataset.
	- If the matcher's input and output are not the same length, you will have to dig into the matcher logs. 
	- If the matcher's input and output are the same length, then a problem happened while exporting the master table to place where the matcher reads it. Check the `webapp` logs for any errors that may have happened while doing this.
- If the results are the same length, then a problem happened while joining the matching results into the database. Check the `webapp_worker` logs for any messages that match those under the (match_finished)[https://github.com/dssg/matching-tool/blob/master/webapp/webapp/tasks.py#L395-L430] code path. 
