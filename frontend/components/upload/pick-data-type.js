import React from 'react'
import RaisedButton from 'material-ui/RaisedButton'
import { selectEventType } from '../../actions'
import { connect } from 'react-redux'
import { validEventTypes } from '../../utils/event-types'
import { map } from 'ramda'


function mapStateToProps(state) {
  return {
    selectedEventType: state.app.selectedEventType,
    availableeventTypes: validEventTypes(
      state.app.availableJurisdictionalRoles,
      state.app.selectedJurisdiction
    )
  }
}

function mapDispatchToProps(dispatch) {
  return {
    selectEventType: (providerType) => {
      return () => {
        dispatch(selectEventType(providerType))
      }
    },
  }
}


const styles = {
  button: { margin: 12, },
  step: { marginLeft: 75 }
}

class PickDataType extends React.Component {
  renderEventTypeButtons() {
    const renderProviderButton = (provider) => {
      return (
        <RaisedButton
          style={styles.button}
          label={provider.name}
          primary={this.props.selectedEventType.slug === provider.slug}
          onMouseUp={this.props.selectEventType(provider)}
          key={provider.slug}
        />
      )
    }
    return map(renderProviderButton, this.props.availableeventTypes)
  }
  render() {
    return (
      <div style={styles.step}><h4>What type of data do you want to upload?</h4>
        {this.renderEventTypeButtons()}
      </div>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(PickDataType)
