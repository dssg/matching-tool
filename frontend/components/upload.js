import React from 'react'
import { bindActionCreators } from 'redux'
import { makeDataGood, makeDataBad } from '../actions'
import RaisedButton from 'material-ui/RaisedButton'
import { connect } from 'react-redux'


function mapStateToProps(state) {
  return {
    status: state.app.data.status,
    reason: state.app.data.reason
  }
}

function mapDispatchToProps(dispatch) {
  return {
    makeDataGood: () => {
      dispatch(makeDataGood('because it is good'))
    },
    makeDataBad: () => {
      dispatch(makeDataBad('because it is bad'))
    }
  }
}

class Upload extends React.Component {
  render() {
    return (
      <div>
        <h2>Upload</h2>
        <RaisedButton label="Good" onMouseUp={this.props.makeDataGood}/>
        <RaisedButton label="Bad" onMouseUp={this.props.makeDataBad}/>
        <div>status: {this.props.status}</div>
        <div>reason: {this.props.reason}</div>
      </div>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(Upload)
