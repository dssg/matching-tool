export default (props) => {
  return (
    <div>
      <p><b>matched_id</b> The identifier generated for this person by the most recent matching process. Will not be stable across runs of the matcher</p>
      <p><b>jail_id</b> The person identifier from the uploaded jail bookings dataset</p>
      <p><b>hmis_id</b> The person identifier from the uploaded hmis service stays dataset</p>
      <p><b>first_name</b> The first name of the person, selected by sorting the first names from all events alphabetically and choosing the last one from that list</p>
      <p><b>last_name</b> The last name of the person, selected by sorting the last names from all events alphabetically and choosing the last one from that list</p>
      <p><b>last_jail_contact</b> The most recent jail entry date associated with this person</p>
      <p><b>last_hmis_contact</b> The most recent client location start date associated with this person</p>
      <p><b>jail_contact</b> The number of jail bookings with any days in the specified time window for this person</p>
      <p><b>hmis_contact</b> The number of HMIS service stays with any days in the specified time window for this person</p>
      <p><b>total_contact</b> The number of jail bookings and HMIS service stays with any days in the specified time window for this person</p>
      <p><b>cumu_jail_days</b> The cumulative number of days associated with all jail bookings with any days in the specified time window for this person. All days associated with the booking will be counted, even if the booking is only partially within the specified time window.  If the booking had not yet ended as of upload time, the upload time is used as the end time.</p>
      <p><b>cumu_hmis_days</b> The cumulative number of days associated with all HMIS service stays with any days in the specified time window for this person. All days associated with the stay will be counted, even if the stay is only partially within the specified time window.  If the stay had not yet ended as of upload time, the upload time is used as the end time.</p>
    </div>
  )
}
