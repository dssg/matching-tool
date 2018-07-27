# Updating the Tool

## User and Role Management

Access to the matching tool web application is handled with users and roles.

A **user** is anybody who can log into the tool.

A **role** is a specific function of the tool that can be accessed by users. In the matching tool, this is the combination of two things: A `jurisdiction` (e.g. your county) and `event_type` (e.g. hmis_service_stays).

The matching-tool repository comes with a convenience script for adding users and roles that aims to make the usual use case (one jurisdiction, with users who have access to many roles) easier. This was run as part of the [install docs](install.md), and you can use it later to add more users.

It is located in the repository path `/scripts/3_create_user`. To run it, you need the following information:

- A short, lowercase name for your jurisdiction (e.g. 'cook'). Don't include spaces as it will confuse the script. This is the name that is displayed to the user in the browser at the top of the screen. This should match whatever jurisdiction name that was picked on initial tool installation. If you don't know what this is, you can query the `public.role` table in the webapp database to see what role names exist.
- An email address for the web app login user
- A password for the web app login user
- A list of 'event types' that the user will have access to upload (e.g. `hmis_service_stays`, `jail_bookings`). If you want to see all the available event types, run the script without any to see the full list (e.g. `./scripts/3_create_user`)
Example: `./scripts/3_create_user mycounty thcrockett@uchicago.edu password hmis_service_stays jail_bookings`

The script tries to create all the resources it needs, even if they exist already, so when the script is running you may see some error messages indicating that roles already exist.

There are some management use cases that are unserved by this script, for instance removing roles from an existing user. If you want more direct control over users and roles, refer to the [webapp readme](https://github.com/dssg/matching-tool/blob/master/webapp/README.md).
