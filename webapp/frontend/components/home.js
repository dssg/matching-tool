import FlatButton from 'material-ui/FlatButton';
import Header from './header'
import React from 'react'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import {Link} from 'react-router-dom'


const styles = {
  page: {
    margin: '50px'
  },
  container: {
    display: 'flex',
    justifyContent: 'space-between',
    width: '50%'
  },
  card: {
    width: '40%',
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
          <div style={styles.container}>
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
        </div>
      </div>
    )
  }
})
