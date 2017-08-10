import React from 'react'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';


const styles = {
  page: {
    margin: '50px'
  },
  container: {
    display: 'flex',
    'justify-content': 'space-between',
    width: '50%'
  },
  card: {
    width: '40%',
  }
}
export default React.createClass({
  render: function() {
    return (
      <div style={styles.page}>
        <h2>Integrating HMIS and Criminal Justice Data</h2>
        <div style={styles.container}>
          <Card style={styles.card}>
            <CardTitle title='Upload' />
            <CardText>
              Some text here explaining something about uploading Some text here explaining something about uploading Some text here explaining something about uploading
            </CardText>
          </Card>
          <Card style={styles.card}>
            <CardTitle title='Charts' />
            <CardText>
              Some text here explaining something about charts Some text here explaining something about charts Some text here explaining something about charts
            </CardText>
          </Card>
        </div>
      </div>
    )
  }
})
