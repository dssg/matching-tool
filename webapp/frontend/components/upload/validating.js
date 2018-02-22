import React from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'
import RaisedButton from 'material-ui/RaisedButton'
import { getValidatedResult } from '../../actions'


const styles = {
  button: { margin: 12, },
  step: { marginLeft: 75 }
}


function mapStateToProps(state) {
  return {
    jobKey: state.app.uploadResponse.jobKey,
    uploadResponse: state.app.uploadResponse,
    message: state.app.uploadResponse.message
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

  handleClick = () => {
    this.props.getValidatedResult(this.props.jobKey)
  }

  render() {
    return (
      <div style={styles.step}>
        <p>{this.props.message} {this.props.jobKey}</p>
        <RaisedButton
          style={styles.button}
          label="Check"
          onClick={this.handleClick} />
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
