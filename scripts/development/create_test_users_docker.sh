docker exec -it webapp alembic upgrade head
docker exec -it webapp flask users create --password password -a testuser@example.com
docker exec -it webapp flask roles create test_hmis_service_stays
docker exec -it webapp flask roles create test_jail_bookings
docker exec -it webapp flask roles create test_by_name_list
docker exec -it webapp flask roles create test_hmis_aliases
docker exec -it webapp flask roles create test_jail_booking_aliases
docker exec -it webapp flask roles create test_jail_booking_charges
docker exec -it webapp flask roles create test_case_charges
docker exec -it webapp flask roles add testuser@example.com test_hmis_service_stays
docker exec -it webapp flask roles add testuser@example.com test_jail_bookings
docker exec -it webapp flask roles add testuser@example.com test_by_name_list
docker exec -it webapp flask roles add testuser@example.com test_hmis_aliases
docker exec -it webapp flask roles add testuser@example.com test_jail_booking_aliases
docker exec -it webapp flask roles add testuser@example.com test_jail_booking_charges
docker exec -it webapp flask roles add testuser@example.com test_case_charges

docker exec -it webapp flask users create --password password -a countyone@example.com
docker exec -it webapp flask roles create countyone_hmis
docker exec -it webapp flask roles add countyone@example.com countyone_hmis

docker exec -it webapp flask users create --password password -a countytwo@example.com
docker exec -it webapp flask roles create countytwo_hmis
docker exec -it webapp flask roles add countytwo@example.com countytwo_hmis
