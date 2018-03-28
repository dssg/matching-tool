import React from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'
import RaisedButton from 'material-ui/RaisedButton'
import { getValidatedResult } from '../../actions'
import CircularProgress from 'material-ui/CircularProgress'

const styles = {
  button: { margin: 12, },
  step: { marginLeft: 75 }
}


function mapStateToProps(state) {
  return {
    jobKey: state.app.validationResponse.jobKey,
    message: state.app.validationResponse.message,
    validationResponse: state.app.validationResponse,
    rowCount: state.app.uploadResponse.rowCount
  }
}


function mapDispatchToProps(dispatch) {
  return {
    getValidatedResult: (jobKey) => {
      dispatch(getValidatedResult(jobKey))
    },
  }
}


class Validating extends React.Component {
  startPoll = () => {
    this.timeout = setTimeout(() => this.props.getValidatedResult(this.props.jobKey), 1000)
  }

  componentWillReceiveProps(nextProps) {
    if (!this.props.isFetching) {
        this.startPoll()
    }
  }

  componentWillMount() {
    this.props.getValidatedResult(this.props.jobKey)
  }

  componentWillUnmount() {
    clearTimeout(this.timeout);
  }

  render() {
    return (
      <div style={styles.step}>
        <p>{this.props.message}</p>
        <div>
          <CircularProgress size={60} thickness={7} />
        </div>
        <Link to="/">
          <RaisedButton
            style={styles.button}
            label="Back to Home" />
          </Link>
      </div>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(Validating)
