docker exec -it webapp alembic upgrade head
docker exec -it webapp flask users create --password password -a example@example.com
docker exec -it webapp flask roles create test_hmis_service_stays
docker exec -it webapp flask roles create test_jail_bookings
docker exec -it webapp flask roles add tweddielin@gmail.com test_jail_bookings
docker exec -it webapp flask roles add tweddielin@gmail.com test_hmis_service_stays
