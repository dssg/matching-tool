import React from 'react'
import { bindActionCreators } from 'redux'
import { selectServiceProvider, resetServiceProvider, changeUploadState, resetUploadState, saveUploadResponse, resetUploadResponse, pickFile, confirmUpload } from '../actions'
import RaisedButton from 'material-ui/RaisedButton'
import Divider from 'material-ui/Divider'
import Paper from 'material-ui/Paper'
import {
  Step,
  Stepper,
  StepLabel,
  StepContent
} from 'material-ui/Stepper'
import WarningIcon from 'material-ui/svg-icons/alert/warning';
import {red500} from 'material-ui/styles/colors';
import { connect } from 'react-redux'
import Upload from 'material-ui-upload/Upload'
import UploadSuccessPage from './upload-success'
import {Link} from 'react-router-dom'
import UploadInvalidPage from './upload-invalid'
import UploadConfirmPage from './upload-confirm'
import Header from './header'
import ReactUploadFile from 'react-upload-file'
import { validServiceProviders } from '../utils/service-providers'
import { map } from 'ramda'


function mapStateToStep(state) {
  if(state.app.selectedServiceProvider.slug === '') {
    return 0
  } else if (state.app.uploadResponse.status === '' || state.app.uploadResponse.status === 'invalid' || state.app.uploadResponse.status === 'error') {
    return 1
  } else if (state.app.mergeResults.totalUniqueRows !== '') {
    return 3
  } else if (state.app.uploadResponse.status === 'valid') {
    return 2
  }
}

function mapStateToProps(state) {
  return {
    selectedServiceProvider: state.app.selectedServiceProvider,
    selectedJurisdiction: state.app.selectedJurisdiction,
    availableServiceProviders: validServiceProviders(
      state.app.availableJurisdictionalRoles,
      state.app.selectedJurisdiction
    ),
    totalUniqueRows: state.app.mergeResults.totalUniqueRows,
    newUniqueRows: state.app.mergeResults.newUniqueRows,
    filePicked: state.app.filePicked,
    uploadFailed: state.app.uploadResponse.status === 'invalid',
    uploadError: state.app.uploadResponse.status === 'error',
    uploadProblem: ['invalid', 'error'].includes(state.app.uploadResponse.status ),
    exampleRows: state.app.uploadResponse.exampleRows,
    fieldOrder: state.app.uploadResponse.fieldOrder,
    numRows: state.app.uploadResponse.rowCount,
    uploadId: state.app.uploadResponse.uploadId,
    step: mapStateToStep(state)
  }
}

function mapDispatchToProps(dispatch) {
  return {
    selectServiceProvider: (providerType) => {
      return () => {
        dispatch(selectServiceProvider(providerType))
      }
    },
    resetToStep0: () => {
      dispatch(resetUploadResponse())
      dispatch(resetServiceProvider())
      dispatch(pickFile(''))
    },
    confirm: (uploadId) => {
      return () => {
        dispatch(confirmUpload(uploadId))
      }
    },
    pickFile: (files) => {
      dispatch(pickFile(files[0].name))
    },
    resetFile: () => {
      dispatch(pickFile(''))
    },
    saveUploadResponse: (uploadResponse) => {
      dispatch(saveUploadResponse(JSON.parse(uploadResponse)))
    },
    resetUploadResponse: () => {
      dispatch(resetUploadResponse())
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
  button: { margin: 12, },
  disabledButton: { margin: 12 },
  step: {
    marginLeft: 75
  }
}

class UploadPage extends React.Component {
  options() {
    return {
      baseUrl: 'api/upload/upload_file',
      withCredentials: true,
      didChoose: this.props.pickFile,
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
  componentWillUnmount() {
    this.props.resetUploadResponse()
    this.props.resetFile()
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
  renderStep0() {
    return (
      <div style={styles.step}><h4>What type of data do you want to upload?</h4>
        {this.renderServiceProviderButtons()}
      </div>
    )
  }
  renderStep1() {
    if(this.props.uploadFailed) {
      return (<UploadInvalidPage />)
    } else if(this.props.uploadError) {
      return (<div>Oops! There was an unexpected error when uploading. This error has been logged</div>)
    } else {
      return (
        <div style={styles.step}>
          <h4>Pick {this.props.selectedServiceProvider.name} file</h4>
          <ReactUploadFile
            options={this.options()}
            chooseFileButton={<RaisedButton style={styles.button} label="Browse for File" />}
            uploadFileButton={<RaisedButton
              disabled={this.props.filePicked === ''}
              primary={this.props.filePicked !== ''}
              style={styles.button}
              label={"Upload " + this.props.filePicked}
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
  renderStep2() {
    return (
      <div style={styles.step}>
        <h2>Upload Confirmation</h2>
        <p>Your {this.props.selectedServiceProvider.name} file was successfully validated. {this.props.numRows} valid rows were found.</p>
        <p>Verify that the first ten rows shown below uploaded in the way you expect. If you are satisfied then click 'Confirm Upload' below, or else click 'Cancel Upload' to try again.</p>
        <Reactable.Table
          className="table"
          data={this.props.exampleRows}
          columns={this.props.fieldOrder} />
        <RaisedButton onMouseUp={this.props.confirm(this.props.uploadId)} style={styles.button} label="Confirm Upload" />
        <RaisedButton
          label="Cancel Upload"
          onClick={this.props.resetToStep0}
          style={styles.button}
        />
      </div>
    )
  }

  renderStep3() {
    return (
      <div style={styles.step}>Your upload has been confirmed. We found {this.props.totalUniqueRows} total unique rows in the upload file, and {this.props.newUniqueRows} that hadn't been uploaded before. Your data is now being sent to our matching service, and may take several hours to process. The matched results, when complete, will be available at the results page.<Link to="/"><RaisedButton label="Back to Home" /></Link></div>)
  }
  renderStepContent() {
    switch (this.props.step) {
      case 0:
        return this.renderStep0()
      case 1:
        return this.renderStep1()
      case 2:
        return this.renderStep2()
      case 3:
        return this.renderStep3()
      default:
        return 'unknown step'
    }
  }
  renderForm() {
    const selectedServiceProvider = this.props.selectedServiceProvider.name
    return (
      <div>
      <div style={styles.section}>
        <h2>Upload</h2>
        <Stepper activeStep={this.props.step}>
          <Step>
            <StepLabel>Choose Data Type</StepLabel>
          </Step>
          <Step>
            <StepLabel
              icon={this.props.uploadProblem ? <WarningIcon color={red500} /> : 2}
              style={this.props.uploadProblem ? {color: red500} : {}}
            >Upload File
            </StepLabel>
          </Step>
          <Step>
            <StepLabel>Confirm Upload</StepLabel>
          </Step>
          <Step>
            <StepLabel>Done!</StepLabel>
          </Step>
        </Stepper>
      </div>
        <div>{this.renderStepContent()}</div>
      </div>
    )
  }

  render() {
    return (<div><Header location={this.props.location} />{this.renderForm()}</div>)
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(UploadPage)
