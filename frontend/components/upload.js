import React from 'react'
import { bindActionCreators } from 'redux'
import { selectServiceProvider, changeUploadState, resetUploadState, saveUploadResponse } from '../actions'
import RaisedButton from 'material-ui/RaisedButton'
import Divider from 'material-ui/Divider'
import Paper from 'material-ui/Paper'
import { connect } from 'react-redux'
import Upload from 'material-ui-upload/Upload'
import UploadSuccessPage from './upload-success'
import UploadInvalidPage from './upload-invalid'
import UploadConfirmPage from './upload-confirm'
import Header from './header'
import ReactUploadFile from 'react-upload-file'
import { validServiceProviders } from '../utils/service-providers'
import { map } from 'ramda'


function mapStateToProps(state) {
  return {
    selectedServiceProvider: state.app.selectedServiceProvider,
    selectedJurisdiction: state.app.selectedJurisdiction,
    availableServiceProviders: validServiceProviders(
      state.app.availableJurisdictionalRoles,
      state.app.selectedJurisdiction
    ),
    showForm: state.app.uploadResponse.status === '',
    showSucceeded: state.app.uploadResponse.status === 'succeeded',
    showConfirm: state.app.uploadResponse.status === 'valid',
    showFailed: state.app.uploadResponse.status === 'invalid',
    showError: state.app.uploadResponse.status === 'error'
  }
}

function mapDispatchToProps(dispatch) {
  return {
    selectServiceProvider: (providerType) => {
      return () => {
        dispatch(selectServiceProvider(providerType))
      }
    },
    saveUploadResponse: (uploadResponse) => {
      dispatch(saveUploadResponse(JSON.parse(uploadResponse)))
    },
    failUpload: () => {
      return () => {
        dispatch(changeUploadState('failed'))
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

const didChoose = (files) => {
  console.log('chose!')
  console.log(files)
}

const beforeUpload = (files) => {
  console.log('before upload!')
  console.log(files)
  return true;
}

const didUpload = (files, xhrId) => {
  console.log('upload!')
  console.log(files)
  console.log(xhrId)
}

const uploadSuccess = (res) => {
  console.log('upload success!')
  console.log(res)
}

const styles = {
  section: { margin: '25px' },
  button: { margin: 12 }
}

class UploadPage extends React.Component {
  options() {
    return {
      baseUrl: 'upload_file',
      withCredentials: true,
      didChoose: didChoose,
      beforeUpload: beforeUpload,
      didUpload: didUpload,
      uploadSuccess: this.props.saveUploadResponse,
      query: () => {
        return {
          jurisdiction: this.props.selectedJurisdiction.slug,
          serviceProvider: this.props.selectedServiceProvider.slug
        }
      }
    }
  }
  renderServiceProviderButtons() {
    const renderProviderButton = (provider) => {
      return (
        <RaisedButton
          style={styles.button}
          label={provider.name}
          primary={this.props.selectedServiceProvider.slug === provider.slug}
          onMouseUp={this.props.selectServiceProvider(provider)}
          key={provider.slug}
        />
      )
    }
    return map(renderProviderButton, this.props.availableServiceProviders)
  }
  renderForm() {
    return (
      <div style={styles.section}>
        <h2>Upload</h2>
        <h4>What type of data do you want to upload?</h4>
        {this.renderServiceProviderButtons()}
        <h4>Upload {this.props.selectedServiceProvider.name} file</h4>

        <ReactUploadFile
          options={this.options()}
          chooseFileButton={<RaisedButton style={styles.button} label="Browse for File" />}
          uploadFileButton={<RaisedButton style={styles.button} label="Upload" />}
        />
        <br />
        <h4>Not sure how to format {this.props.selectedServiceProvider.name} file?</h4>
        <RaisedButton
          style={styles.button}
          label="View Input File Schema"
        />
      </div>
    )
  }

  render() {
    if (this.props.showForm) {
      return (<div><Header location={this.props.location} />{this.renderForm()}</div>)
    } else if (this.props.showSucceeded) {
      return (<div><Header location={this.props.location} /><UploadSuccessPage /></div>)
    } else if (this.props.showConfirm) {
      return (<div><Header location={this.props.location} /><UploadConfirmPage /></div>)
    } else if (this.props.showError) {
      return (<div><Header location={this.props.location} />Oops! There was an unexpected error when uploading. The error has been logged.</div>)
    } else {
      return (<div><Header location={this.props.location} /><UploadInvalidPage /></div>)
    }
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(UploadPage)
