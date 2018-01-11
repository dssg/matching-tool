import React from 'react'
import { resetUploadResponse, pickFile } from '../actions'
import PickDataType from './upload/pick-data-type'
import UploadFile from './upload/upload-file'
import ConfirmData from './upload/confirm-data'
import Done from './upload/done'
import { Step, Stepper, StepLabel } from 'material-ui/Stepper'
import WarningIcon from 'material-ui/svg-icons/alert/warning'
import {red500} from 'material-ui/styles/colors'
import { connect } from 'react-redux'
import Header from './header'


function mapStateToStep(state) {
  if(state.app.selectedEventType.slug === '') {
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
    uploadProblem: ['invalid', 'error'].includes(state.app.uploadResponse.status ),
    step: mapStateToStep(state)
  }
}

function mapDispatchToProps(dispatch) {
  return {
    resetFile: () => {
      dispatch(pickFile(''))
    },
    resetUploadResponse: () => {
      dispatch(resetUploadResponse())
    },
  }
}

const styles = {
  section: { margin: '25px' },
}

class UploadPage extends React.Component {
  componentWillUnmount() {
    this.props.resetUploadResponse()
    this.props.resetFile()
  }

  renderStepContent() {
    switch (this.props.step) {
    case 0: return (<PickDataType />)
    case 1: return (<UploadFile />)
    case 2: return (<ConfirmData />)
    case 3: return (<Done />)
    default: return 'unknown step'
    }
  }

  render() {
    return (
      <div>
        <Header location={this.props.location} />
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
          <div>{this.renderStepContent()}</div>
        </div>
      </div>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(UploadPage)
