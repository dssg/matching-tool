import React from 'react'
import RaisedButton from 'material-ui/RaisedButton'
import { selectServiceProvider } from '../../actions'
import { connect } from 'react-redux'
import { validServiceProviders } from '../../utils/service-providers'
import { map } from 'ramda'


function mapStateToProps(state) {
  return {
    selectedServiceProvider: state.app.selectedServiceProvider,
    availableServiceProviders: validServiceProviders(
      state.app.availableJurisdictionalRoles,
      state.app.selectedJurisdiction
    )
  }
}

function mapDispatchToProps(dispatch) {
  return {
    selectServiceProvider: (providerType) => {
      return () => {
        dispatch(selectServiceProvider(providerType))
      }
    },
  }
}


const styles = {
  button: { margin: 12, },
  step: { marginLeft: 75 }
}

class PickDataType extends React.Component {
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
  render() {
    return (
      <div style={styles.step}><h4>What type of data do you want to upload?</h4>
        {this.renderServiceProviderButtons()}
      </div>
    )
  }
}
export default connect(mapStateToProps, mapDispatchToProps)(PickDataType)
