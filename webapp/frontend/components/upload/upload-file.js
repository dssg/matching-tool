import React from 'react'
import RaisedButton from 'material-ui/RaisedButton'
import ReactUploadFile from 'react-upload-file'
import { pickFile, resetEventType, resetUploadResponse, saveUploadResponse } from '../../actions'
import UploadInvalid from './invalid'
import CircularProgress from 'material-ui/CircularProgress'
import { connect } from 'react-redux'


function mapStateToProps(state) {
  return {
    selectedEventType: state.app.selectedEventType,
    selectedJurisdiction: state.app.selectedJurisdiction,
    uploadValidating: state.app.validationResponse.status === 'validating',
    uploadFailed: state.app.validationResponse.status === 'invalid',
    uploadError: state.app.uploadResponse.status === 'error',
    filePicked: state.app.filePicked,
    jobKey: state.app.validationResponse.jobKey,
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


class UploadFile extends React.Component {
  constructor(props) {
    super(props);
    this.state = {uploading: false};
  }
  options() {
    return {
      baseUrl: 'api/upload/upload_file',
      withCredentials: true,
      didChoose: this.props.pickFile,
      beforeUpload: (files) => {
        this.setState({uploading: true})
        return files
      },
      uploadSuccess: (uploadResponse) => {
        this.setState({uploading: false})
        this.props.saveUploadResponse(uploadResponse)
      },
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
    } else if(this.props.uploadValidating) {
      return (<div>The uploader is validating! job key is {this.props.jobKey}</div>)
    } else {
      const label = this.state.uploading === true ? 'Uploading ' + this.props.filePicked + ' ...' : 'Upload ' + this.props.filePicked
      return (
        <div style={styles.step}>
          <h4>Pick {this.props.selectedEventType.name} file</h4>
          {this.state.uploading === true ? <span><p>{label}</p><div><CircularProgress size={60} thickness={7} /></div></span> : null}
          <ReactUploadFile
            options={this.options()}
            chooseFileButton={<RaisedButton
              style={styles.button}
              label="Browse for File"
              disabled={this.state.uploading === true}
            />}
            uploadFileButton={<RaisedButton
              disabled={this.props.filePicked === '' || this.state.uploading === true}
              primary={this.props.filePicked !== ''}
              style={styles.button}
              label={label}
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
