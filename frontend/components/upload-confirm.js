import React from 'react'
import { selectServiceProvider } from '../actions'
import { Link } from 'react-router-dom'
import RaisedButton from 'material-ui/RaisedButton'
import Divider from 'material-ui/Divider'
import Paper from 'material-ui/Paper'
import { connect } from 'react-redux'
import Upload from 'material-ui-upload/Upload'
import Reactable from 'reactable'


function mapStateToProps(state) {
  return {
    serviceProvider: state.app.serviceProvider,
    exampleRows: state.app.uploadResponse.exampleRows,
    numRows: state.app.uploadResponse.rowCount
  }
}

function mapDispatchToProps(dispatch) {
  return {
  }
}
const sampleUsers = [
  {
    'Internal Person ID': 'A023918475',
    'Internal Event ID': '248458',
    'Full Name': 'Henrik Zetterberg',
    'Birthdate': '1980-02-01',
    'DMV Number': 'S-123-4567-7890',
  },
  {
    'Internal Person ID': 'A023918476',
    'Internal Event ID': '248459',
    'Full Name': 'Dylan Larkin',
    'Birthdate': '1980-03-01',
    'DMV Number': 'S-123-4567-7891',
  },
  {
    'Internal Person ID': 'A023918477',
    'Internal Event ID': '248460',
    'Full Name': 'Petr Mrazek',
    'Birthdate': '1980-04-01',
    'DMV Number': 'S-123-4567-7892',
  },
  {
    'Internal Person ID': 'A023918478',
    'Internal Event ID': '248461',
    'Full Name': 'Jimmy Howard',
    'Birthdate': '1980-05-01',
    'DMV Number': 'S-123-4567-7893',
  },
  {
    'Internal Person ID': 'A023918479',
    'Internal Event ID': '248462',
    'Full Name': 'Tomas Tatar',
    'Birthdate': '1980-06-01',
    'DMV Number': 'S-123-4567-7894',
  },
  {
    'Internal Person ID': 'A023918480',
    'Internal Event ID': '248463',
    'Full Name': 'Justin Abdelkader',
    'Birthdate': '1980-07-01',
    'DMV Number': 'S-123-4567-7895',
  },
  {
    'Internal Person ID': 'A023918481',
    'Internal Event ID': '248464',
    'Full Name': 'Andreas Athanasiou',
    'Birthdate': '1980-08-01',
    'DMV Number': 'S-123-4567-7896',
  },
  {
    'Internal Person ID': 'A023918482',
    'Internal Event ID': '248465',
    'Full Name': 'Anthony Mantha',
    'Birthdate': '1980-09-01',
    'DMV Number': 'S-123-4567-7897',
  },
  {
    'Internal Person ID': 'A023918483',
    'Internal Event ID': '248466',
    'Full Name': 'Niklas Kronwall',
    'Birthdate': '1980-10-01',
    'DMV Number': 'S-123-4567-7898',
  },
  {
    'Internal Person ID': 'A023918484',
    'Internal Event ID': '248467',
    'Full Name': 'Gustav Nyquist',
    'Birthdate': '1980-11-01',
    'DMV Number': 'S-123-4567-7899',
  },
]

const styles = {
  section: { margin: '25px' },
  button: { margin: 12 }
}

class UploadConfirmPage extends React.Component {
  render() {
    return (
      <div style={styles.section}>
        <h2>Upload Confirmation</h2>
        <p>Your {this.props.serviceProvider} file was successfully validated. {this.props.numRows} valid rows were found.</p>
        <p>Verify that the first ten rows shown below uploaded in the way you expect. If you are satisfied then click 'Confirm Upload' below, or else click 'Cancel Upload' to try again.</p>
        <Reactable.Table
          className="table"
          data={this.props.exampleRows} />
        <Link to='/results'><RaisedButton style={styles.button} label="Confirm Upload" /></Link>
        <Link to='/results'><RaisedButton style={styles.button} label="Cancel Upload" /></Link>
      </div>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(UploadConfirmPage)
