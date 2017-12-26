import React from 'react'
import RaisedButton from 'material-ui/RaisedButton'
import ReactUploadFile from 'react-upload-file'
import { pickFile, resetEventType, resetUploadResponse, saveUploadResponse } from '../../actions'
import UploadInvalid from './invalid'
import { connect } from 'react-redux'


function mapStateToProps(state) {
  return {
    selectedEventType: state.app.selectedEventType,
    selectedJurisdiction: state.app.selectedJurisdiction,
    uploadFailed: state.app.uploadResponse.status === 'invalid',
    uploadError: state.app.uploadResponse.status === 'error',
    filePicked: state.app.filePicked,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    resetToStep0: () => {
      dispatch(resetUploadResponse())
      dispatch(resetEventType())
      dispatch(pickFile(''))
    },
    pickFile: (files) => {
      dispatch(pickFile(files[0].name))
    },
    saveUploadResponse: (uploadResponse) => {
      dispatch(saveUploadResponse(JSON.parse(uploadResponse)))
    },
  }
}


const styles = {
  button: { margin: 12, },
  step: { marginLeft: 75 }
}


const beforeUpload = (files) => {
  return true;
}

class UploadFile extends React.Component {
  options() {
    return {
      baseUrl: 'api/upload/upload_file',
      withCredentials: true,
      didChoose: this.props.pickFile,
      beforeUpload: beforeUpload,
      uploadSuccess: this.props.saveUploadResponse,
      query: () => {
        return {
          jurisdiction: this.props.selectedJurisdiction.slug,
          eventType: this.props.selectedEventType.slug
        }
      }
    }
  }
  render() {
    if(this.props.uploadFailed) {
      return (<UploadInvalid />)
    } else if(this.props.uploadError) {
      return (<div>Oops! There was an unexpected error when uploading. This error has been logged</div>)
    } else {
      return (
        <div style={styles.step}>
          <h4>Pick {this.props.selectedEventType.name} file</h4>
          <ReactUploadFile
            options={this.options()}
            chooseFileButton={<RaisedButton style={styles.button} label="Browse for File" />}
            uploadFileButton={<RaisedButton
              disabled={this.props.filePicked === ''}
              primary={this.props.filePicked !== ''}
              style={styles.button}
              label={'Upload ' + this.props.filePicked}
            />}
          />
          <br />
          <RaisedButton
            label="Back"
            onClick={this.props.resetToStep0}
            style={styles.button}
          />
        </div>
      )
    }
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(UploadFile)
