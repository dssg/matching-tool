function pyexec() {
	python3 - <<END
import boto
conn = boto.connect_s3();
conn.create_bucket('your-bucket')
END
}

pyexec
