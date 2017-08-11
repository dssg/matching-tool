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
        <h2>Charts</h2>
        <div style={styles.container}>
          <h4> Test </h4>
        </div>
      </div>
    )
  }
})