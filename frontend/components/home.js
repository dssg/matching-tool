import React from 'react'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';

export default React.createClass({
  render: function() {
    return (
      <div>
        <h2>Integrating HMIS and Criminal Justice Data</h2>
        <div>
          <Card style={{width: '25%'}}>
            <CardTitle title='Upload' />
            <CardText>
              Some text here explaining something about uploading
            </CardText>
          </Card>
          <Card style={{width: '25%'}}>
            <CardTitle title='Charts' />
            <CardText>
              Some text here explaining something about charts
            </CardText>
          </Card>
        </div>
      </div>
    )
  }
})
