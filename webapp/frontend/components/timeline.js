import React from 'react'
import { connect } from 'react-redux'
import { Timeline, TimelineEvent } from 'react-event-timeline'
import { getAllJobs } from '../actions'


const styles = {
  timeline: {
    height: '600px',
    overflow: 'scroll'
  }
}

function mapStateToProps(state) {
  return {
    current: state.app.allJobs.current,
    q: state.app.allJobs.q
  }
}

function mapDispatchToProps(dispatch) {
  return {
    updateAllJobs: () => {
      dispatch(getAllJobs())
    }
  }
}

class ActionTimeLine extends React.Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    this.props.updateAllJobs()
  }

  render() {
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
                  <p><strong>Current Runtime: </strong> 4 hours</p>
                  <p><strong>Service Type: </strong>HMIS</p>
                  <p><strong>File Name: </strong>slc_hmis_03152018.csv</p>
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
                  <p><strong>Service Type: </strong>HMIS</p>
                  <p><strong>File Name: </strong>slc_hmis_03152018.csv</p>
                </div>
              </TimelineEvent>
            ))}
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
      </div>
    )
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(ActionTimeLine)

