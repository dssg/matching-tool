import React from 'react'
import { bindActionCreators } from 'redux'
import { selectServiceProvider } from '../actions'
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
    selectServiceProvider: (providerType) => {
      return () => {
        dispatch(selectServiceProvider(providerType))
      }
    },
  }
}

const styles = {
  section: { margin: '25px' },
  button: { margin: 12 }
}
class UploadPage extends React.Component {
  render() {
    return (
      <div style={styles.section}>
        <h2>Upload</h2>
        <h4>What type of data do you want to upload?</h4>
        <RaisedButton style={styles.button} label="HMIS" primary={this.props.serviceProvider === 'HMIS'} onMouseUp={this.props.selectServiceProvider('HMIS')}/>
        <RaisedButton style={styles.button} label="Jail" primary={this.props.serviceProvider === 'Jail'} onMouseUp={this.props.selectServiceProvider('Jail')}/>
        <h4>Upload {this.props.serviceProvider} file</h4>
        <RaisedButton style={styles.button} label="Browse" />
        <br />
        <RaisedButton style={styles.button} label="Upload" />
      </div>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(UploadPage)
