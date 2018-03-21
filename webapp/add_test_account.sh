# create test user
docker exec -it webapp alembic upgrade head
docker exec -it webapp flask users create --password password -a example@example.com
docker exec -it webapp flask roles create test_hmis_service_stays
docker exec -it webapp flask roles create test_jail_bookings
docker exec -it webapp flask roles add example@example.com test_jail_bookings
docker exec -it webapp flask roles add example@example.com test_hmis_service_stays

# create boone_test user
docker exec -it webapp flask users create --password password -a boonetest@example.com
docker exec -it webapp flask roles create boonetest_hmis_service_stays
docker exec -it webapp flask roles create boonetest_jail_bookings
docker exec -it webapp flask roles add boonetest@example.com boonetest_jail_bookings
docker exec -it webapp flask roles add boonetest@example.com boonetest_hmis_service_stays

# create mclean_test user
docker exec -it webapp flask users create --password password -a mcleantest@example.com
docker exec -it webapp flask roles create mcleantest_hmis_service_stays
docker exec -it webapp flask roles create mcleantest_jail_bookings
docker exec -it webapp flask roles add mcleantest@example.com mcleantest_jail_bookings
docker exec -it webapp flask roles add mcleantest@example.com mcleantest_hmis_service_stays

# create slco_test user
docker exec -it webapp flask users create --password password -a slcotest@example.com
docker exec -it webapp flask roles create slcotest_hmis_service_stays
docker exec -it webapp flask roles create slcotest_jail_bookings
docker exec -it webapp flask roles add slcotest@example.com slcotest_jail_bookings
docker exec -it webapp flask roles add slcotest@example.com slcotest_hmis_service_stays
