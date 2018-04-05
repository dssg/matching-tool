import React from 'react'
import { connect } from 'react-redux'
import { Timeline, TimelineEvent } from 'react-event-timeline'
import { getAllJobs, getHistory } from '../actions'


const styles = {
  timeline: {
    height: '600px',
    width: '350px',
    overflow: 'scroll'
  }
}

function mapStateToProps(state) {
  return {
    current: state.app.allJobs.current,
    q: state.app.allJobs.q,
    history: state.app.history
  }
}

function mapDispatchToProps(dispatch) {
  return {
    updateAllJobs: () => {
      dispatch(getAllJobs())
    },
    updateHistory: () => {
      dispatch(getHistory())
    }
  }
}

class ActionTimeLine extends React.Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    this.props.updateAllJobs()
    this.props.updateHistory()
  }

  render() {
    console.log(this.props.history)
    return (
      <div style={styles.timeline}>
        <Timeline>
            {this.props.current.map((item, idx) => (
              <TimelineEvent
                title="Current Tasks Status"
                subtitle="Matching"
                subtitleStyle={{color: "#6fba1c"}}
                icon={<i className="material-icons md-18">build</i>}
                iconColor="#6fba1c"
                key={idx}>
                <div>
                  <p><strong>Upload Time: </strong> {item.created_time}</p>
                  <p><strong>Current Runtime: </strong> {item.runtime}</p>
                  <p><strong>Service Type: </strong>{item.event_type}</p>
                  <p><strong>File Name: </strong>{item.filename}</p>
                </div>
              </TimelineEvent>
            ))}
            {this.props.q.map((item, idx) => (
              <TimelineEvent
                title="Current Tasks Status"
                subtitle="In queue waiting"
                subtitleStyle={{color: "#FBB117"}}
                icon={<i className="material-icons md-18">build</i>}
                iconColor="#FBB117"
                key={idx}>
                <div>
                  <p><strong>Upload Time: </strong> {item.created_time}</p>
                  <p><strong>Current Runtime: </strong> 4 hours</p>
                  <p><strong>Service Type: </strong>{item.event_type}</p>
                  <p><strong>File Name: </strong>{item.given_filename}</p>
                </div>
              </TimelineEvent>
            ))}
            {this.props.history.map((item, idx) => (
              <TimelineEvent
                title="Last Task"
                icon={<i className="material-icons md-18">cloud_upload</i>}
                iconColor="#43C6DB"
                key={idx}>
              <p><strong>Upload Time: </strong> {item.upload_timestamp}</p>
              <p><strong>Matched Time: </strong> {item.match_complete_timestamp}</p>
              <p><strong>Matching Runtime: </strong> {item.runtime}</p>
              <p><strong>Service Type: </strong>{item.event_type_slug}</p>
              <p><strong>File Name: </strong>{item.given_filename}</p>
            </TimelineEvent>
            ))}
        </Timeline>
      </div>
    )
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(ActionTimeLine)
