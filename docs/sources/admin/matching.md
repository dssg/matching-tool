# Configuring the matching service

This document covers the process for administrators to update a deployed matching tool with a new matching configuration file. It does not include a guide for modifying the configuration file itself. For that, see [Modifying the Matching Service](/dev/matching).

Given a new matching configuration file, it can be applied by putting it in the path `/matching-tool/matcher/matcher_config.yaml`, rebuilding and restarting the containers. From that point on, a user can simply upload and merge any file to trigger the matching process again with the new configuration, even a file with only one record.

Example: Given a new matching configuration file called `new_matching.yaml`:

```bash
cp new_matching.yaml matching-tool/matcher/matcher_config.yaml
cd matching-tool
./scripts/run rebuild
./scripts/run start

# At this point the user can upload a one-line file in the web browser to kick off matching.
```
