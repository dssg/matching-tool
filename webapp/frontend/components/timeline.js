import React from 'react'
import { connect } from 'react-redux'
import { Timeline, TimelineEvent } from 'react-event-timeline'
import { getAllJobs, getHistory } from '../actions'
import { filter, prop, keys, values } from 'ramda'

const styles = {
  timeline: {
    height: '600px',
    width: '400px',
    overflow: 'scroll'
  }
}

const lookup = {
  validate_start_time: "Validate Start Time: ",
  validate_complete_time: "Validate Complete Time: ",
  validate_status: "Validate Status: ",
  upload_start_time: "Upload Start Time: ",
  upload_complete_time: "Upload Complete Time: ",
  upload_status: "Upload Status: ",
  match_start_timestamp: "Match Start Time: ",
  match_complete_timestamp: "Match Complete Time: ",
  match_status: "Match Status: ",
  runtime: "Matching Runtime: ",
  event_type_slug: "Service Type: ",
  given_filename: "File Name: "
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

function boolean2text(bool) {
  if (bool) {
    return (
      <font color="#43C6DB">Succeeded</font>
    )
  }
  else {
    return (
      <font color="#ff7456">Failed</font>
    )
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

  createCompletedTask(item, idx) {
    return (
      <TimelineEvent
          title={"Completed Task #" + item.index + " - " + item.validate_start_time}
          icon={<i className="material-icons md-18">cloud_upload</i>}
          iconColor={(item['validate_status'] || item['upload_status']) ? "#43C6DB" : "#ff7456" }
          key={idx}>

        {keys(lookup).map((k) => {
          if (k in item)  {
            if (item[k] !== null) {
              if (k == 'validate_status' || k == 'upload_status' || k == 'match_status') {
                return <p key={k}><strong>{lookup[k]}{boolean2text(item[k])}</strong></p>
              }
              else {
                return <p key={k}><strong>{lookup[k]}</strong>{item[k]}</p>
              }
            }
          }
        }
        )}
      </TimelineEvent>
    )
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
                  <p><strong>Match Start Time: </strong> {item.created_time}</p>
                  <p><strong>Current Runtime: </strong> {item.runtime}</p>
                  <p><strong>Validate Start Time: </strong> {item.meta.validate_start_time}</p>
                  <p><strong>Validate Complete Time: </strong> {item.meta.validate_complete_time}</p>
                  <p><strong>Upload Start Time: </strong> {item.meta.upload_start_time}</p>
                  <p><strong>Upload Complete Time: </strong> {item.meta.upload_complete_time}</p>
                  <p><strong>Service Type: </strong>{item.meta.event_type_slug}</p>
                  <p><strong>File Name: </strong>{item.meta.given_filename}</p>
                </div>
              </TimelineEvent>
            ))}
            {this.props.q.map((item, idx) => (
              <TimelineEvent
                title="Current Tasks Status"
                subtitle="In queue waiting to match"
                subtitleStyle={{color: "#FBB117"}}
                icon={<i className="material-icons md-18">build</i>}
                iconColor="#FBB117"
                key={idx}>
                <div>
                  <p><strong>Validate Start Time: </strong> {item.meta.validate_start_time}</p>
                  <p><strong>Validate Complete Time: </strong> {item.meta.validate_complete_time}</p>
                  <p><strong>Upload Start Time: </strong> {item.meta.upload_start_time}</p>
                  <p><strong>Upload Complete Time: </strong> {item.meta.upload_complete_time}</p>
                  <p><strong>Service Type: </strong>{item.meta.event_type_slug}</p>
                  <p><strong>File Name: </strong>{item.meta.given_filename}</p>
                </div>
              </TimelineEvent>
            ))}
            {this.props.history.map((item, idx) => (
              this.createCompletedTask(item, idx)
            ))}
        </Timeline>
      </div>
    )
  }
}


export default connect(mapStateToProps, mapDispatchToProps)(ActionTimeLine)
