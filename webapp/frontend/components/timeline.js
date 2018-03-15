import React from 'react'
import {Timeline, TimelineEvent} from 'react-event-timeline'

export default class ActionTimeLine extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      matchingStatus: true,
    }
  }
  renderMatchingStatus() {
    if (this.state.matchingStatus) {
      return (
        <div>
          <p><strong>Status:</strong> Finished</p>
          <p><strong>New Unique Rows:</strong> 9</p>
          <p><strong>Total Unique Rows:</strong> 9</p>
          <p><strong>Matching Time:</strong> 00:09:32</p>
        </div>
      )
    } else {
      return (
        <div>
          <p><strong>Status:</strong>Still matching...</p>
        </div>
      )
    }

  }

  render() {
    return (
        <Timeline>
            <TimelineEvent title="Current Matching Status"
                           createdAt="2016-09-12 10:06 PM"
                           icon={<i className="material-icons md-18">build</i>}>
              {this.renderMatchingStatus()}
            </TimelineEvent>
            <TimelineEvent title="Last Uploaded & Matched"
                           createdAt="2016-09-11 09:06 AM"
                           icon={<i className="material-icons md-18">cloud_upload</i>}>
              <p><strong>Service Type:</strong> HMIS</p>
              <p><strong>File Name:</strong> slc_hmis.csv</p>
              <p><strong>File Size:</strong> 6MB</p>
            </TimelineEvent>
      </Timeline>
    )
  }
}
