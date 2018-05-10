import { connect } from 'react-redux'
import downloadURI from '../utils/download-uri'
import { validEventTypes } from '../utils/event-types'
import React from 'react'
import SelectField from 'material-ui/SelectField'
import MenuItem from 'material-ui/MenuItem'
import RaisedButton from 'material-ui/RaisedButton'
import { clone, join, keys, map } from 'ramda'


function mapStateToProps(state) {
  return {
    filters: state.app.matchingFilters,
    availableEventTypes: validEventTypes(
      state.app.availableJurisdictionalRoles,
      state.app.selectedJurisdiction
    )
  }
}
function mapDispatchToProps(dispatch) {
  return {}
}

export class SourceDownloader extends React.Component {
  state = { value: null }

  handleChange = (event, index, value) => {
    this.setState({value}) 
  }

  assembleURLParams = (eventType) => {
    const params = {
      startDate: this.props.filters.startDate,
      endDate: this.props.filters.endDate,
      jurisdiction: this.props.selectedJurisdictionSlug,
      eventType: eventType
    }
    return join('&', map(
      (key) => encodeURIComponent(key) + '=' + encodeURIComponent(params[key]),
      keys(params)
    ))
  }

  downloadSource = (eventType) => {
    const url = '/api/chart/download_source?' + this.assembleURLParams(eventType)
    downloadURI(url)
  }

  handleDownload = () => {
    this.downloadSource(this.state.value)
  }

  renderEventType = (eventType) => {
    return <MenuItem key={eventType.slug} value={eventType.slug} primaryText={eventType.name} />
  }

  renderEventTypes = () => {
    const eventTypes = [{name: "", slug: null}].concat(this.props.availableEventTypes)
    return map(this.renderEventType, eventTypes)
  }
  
  render() {
    return (
      <div>
        <SelectField
          floatingLabelText="Event Type"
          value={this.state.value}
          onChange={this.handleChange}
        >
          {this.renderEventTypes()}
        </SelectField>
        <RaisedButton
          label="Download Source"
          onClick={this.handleDownload}
        />
      </div>
    )
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(SourceDownloader)
