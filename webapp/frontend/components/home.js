import FlatButton from 'material-ui/FlatButton';
import Header from './header'
import React from 'react'
import { Card, CardActions, CardHeader, CardMedia, CardTitle, CardText } from 'material-ui/Card';
import { Link } from 'react-router-dom'
import ActionTimeLine from './timeline'

const styles = {
  page: {
    margin: '50px'
  },
  container: {
    display: 'flex',
    justifyContent: 'space-between',
    width: '65%'
  },
  card: {
    width: '50%',
    margin: '10px'
  },
  title: {
    marginBottom: '40px'
  }
}
export default React.createClass({
  render: function() {
    return (
      <div>
        <Header location={this.props.location} />
        <div style={styles.page}>
          <h2 style={styles.title}>Integrating HMIS and Criminal Justice Data</h2>
          <div className="col-sm-9" style={styles.container}>
            <Card style={styles.card}>
              <Link to='/upload'><CardTitle title='Upload' /></Link>
              <CardText>
                Upload a tabular file (such as a CSV) representing user data from one of your county systems. This data will be securely stored and matched with data from other county systems.
              </CardText>
            </Card>
            <Card style={styles.card}>
              <Link to='/results'><CardTitle title='Results' /></Link>
              <CardText>
                View matched data to find overlaps between populations, and frequent utilizers of county systems.
              </CardText>
            </Card>
          </div>
          <div className="col-sm-3">
              <ActionTimeLine />
          </div>
        </div>
      </div>
    )
  }
})
