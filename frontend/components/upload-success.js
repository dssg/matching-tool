import React from 'react'
import { selectServiceProvider } from '../actions'
import { Link } from 'react-router-dom'
import RaisedButton from 'material-ui/RaisedButton'
import Divider from 'material-ui/Divider'
import Paper from 'material-ui/Paper'
import { connect } from 'react-redux'
import Upload from 'material-ui-upload/Upload'


function mapStateToProps(state) {
  return {
    serviceProvider: state.app.serviceProvider,
  }
}

function mapDispatchToProps(dispatch) {
  return {
  }
}

const styles = {
  section: { margin: '25px' },
  button: { margin: 12 }
}
class UploadSuccessPage extends React.Component {
  render() {
    return (
      <div style={styles.section}>
        <h2>Upload Success</h2>
        <p>Your {this.props.serviceProvider} file was successfully uploaded.</p>
        <p>375 valid rows found</p>
        <Link to='/charts'><RaisedButton style={styles.button} label="View Your Data" /></Link>
      </div>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(UploadSuccessPage)
