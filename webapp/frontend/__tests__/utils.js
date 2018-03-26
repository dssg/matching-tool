import fs from 'fs'

export default function endpointJSON(user, endpoint) {
  var fname = '../sample_data/user_endpoints/' + user + '/' + endpoint
  return JSON.parse(fs.readFileSync(fname))
}
