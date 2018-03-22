import React from 'react'
import { connect } from 'react-redux'
import {Timeline, TimelineEvent} from 'react-event-timeline'

export default class ActionTimeLine extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      matchingStatus: false,
    }
  }
  renderMatchingStatus() {
    if (this.state.matchingStatus) {
      return (
        <TimelineEvent title="Current Task Status"

                       subtitle="Done!"
                       subtitleStyle={{color: "#6fba1c"}}
                       icon={<i className="material-icons md-18">build</i>}
                       iconColor="#6fba1c">
          <div>
            <p><strong>Upload Time: </strong> 2018-03-15 10:06 PM</p>
            <p><strong>Matched Time: </strong> 2018-03-15 11:06 PM</p>
            <p><strong>Service Type: </strong>HMIS</p>
            <p><strong>File Name: </strong>slc_hmis_03152018.csv</p>
            <p><strong>File Size: </strong>67MB</p>
            <p><strong>New Unique Rows: </strong>13000</p>
            <p><strong>Total Unique Rows: </strong>13100</p>
          </div>
        </TimelineEvent>
      )
    } else {
      return (
        <TimelineEvent title="Current Task Status"
                       subtitle="Still matching"
                       subtitleStyle={{color: "#FBB117"}}
                       icon={<i className="material-icons md-18">build</i>}
                       iconColor="#FBB117">
          <div>
            <p><strong>Upload Time: </strong> 2018-03-15 10:06 PM</p>
            <p><strong>Current Runtime: </strong> 4 hours</p>
            <p><strong>Service Type: </strong>HMIS</p>
            <p><strong>File Name: </strong>slc_hmis_03152018.csv</p>
          </div>
        </TimelineEvent>
      )
    }
  }

  render() {
    return (
        <Timeline>
            {this.renderMatchingStatus()}
            <TimelineEvent title="Last Task"
                           icon={<i className="material-icons md-18">cloud_upload</i>}
                           iconColor="#43C6DB">
              <p><strong>Upload Time: </strong> 2018-03-12 10:06 PM</p>
              <p><strong>Matched Time: </strong> 2018-03-12 10:16 PM</p>
              <p><strong>Matching Runtime: </strong> 05:00:00</p>
              <p><strong>Service Type: </strong>HMIS</p>
              <p><strong>File Name: </strong>slc_hmis_03122018.csv</p>
            </TimelineEvent>
      </Timeline>
    )
  }
}
