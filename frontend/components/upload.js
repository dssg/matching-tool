import React from 'react'
import { bindActionCreators } from 'redux'
import { selectServiceProvider, changeUploadState, resetUploadState } from '../actions'
import RaisedButton from 'material-ui/RaisedButton'
import Divider from 'material-ui/Divider'
import Paper from 'material-ui/Paper'
import { connect } from 'react-redux'
import Upload from 'material-ui-upload/Upload'
import UploadSuccessPage from './upload-success'
import UploadInvalidPage from './upload-invalid'
import UploadConfirmPage from './upload-confirm'


function mapStateToProps(state) {
  return {
    serviceProvider: state.app.serviceProvider,
    showForm: state.app.uploadState == '',
    showSucceeded: state.app.uploadState == 'succeeded',
    showConfirm: state.app.uploadState == 'needsConfirmation',
    showFailed: state.app.uploadState == 'failed',
  }
}

function mapDispatchToProps(dispatch) {
  return {
    selectServiceProvider: (providerType) => {
      return () => {
        dispatch(selectServiceProvider(providerType))
      }
    },
    failUpload: () => {
      return () => {
        dispatch(changeUploadState('failed'))
      }
    },
    promptConfirmUpload: () => {
      return () => {
        dispatch(changeUploadState('needsConfirmation'))
      }
    },
    succeedUpload: () => {
      return () => {
        dispatch(changeUploadState('succeeded'))
      }
    },
    resetUpload: () => {
      return () => {
        dispatch(resetUploadState())
      }
    }
  }
}

const styles = {
  section: { margin: '25px' },
  button: { margin: 12 }
}
class UploadPage extends React.Component {
  componentWillMount() {
    console.log('reset upload!')
    this.props.resetUpload() 
  }

  renderForm() {
    return (
      <div style={styles.section}>
        <h2>Upload</h2>
        <h4>What type of data do you want to upload?</h4>
        <RaisedButton style={styles.button} label="HMIS" primary={this.props.serviceProvider === 'HMIS'} onMouseUp={this.props.selectServiceProvider('HMIS')}/>
        <RaisedButton style={styles.button} label="Jail" primary={this.props.serviceProvider === 'Jail'} onMouseUp={this.props.selectServiceProvider('Jail')}/>
        <RaisedButton style={styles.button} label="Other" primary={this.props.serviceProvider === 'Other'} onMouseUp={this.props.selectServiceProvider('Other')}/>
        <h4>Upload {this.props.serviceProvider} file</h4>
        <RaisedButton
          style={styles.button}
          label="Browse for File"
          onMouseUp={this.props.failUpload()}
        />
        <br />
        <RaisedButton
          style={styles.button}
          label="Upload"
          onMouseUp={this.props.succeedUpload()}
        />
        <h4>Not sure how to format {this.props.serviceProvider} file?</h4>
        <RaisedButton
          style={styles.button}
          label="View Input File Schema"
          onMouseUp={this.props.promptConfirmUpload()}
        />
      </div>
    )
  }

  render() {
    if (this.props.showForm) {
      return this.renderForm()
    } else if (this.props.showSucceeded) {
      return (<UploadSuccessPage />)
    } else if (this.props.showConfirm) {
      return (<UploadConfirmPage />)  
    } else {
      return (<UploadInvalidPage />)
    }
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(UploadPage)
