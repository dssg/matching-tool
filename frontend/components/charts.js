import React from 'react'
import d3 from 'd3'
import Venn from './venn'
import Reactable from 'reactable'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import FlatButton from 'material-ui/FlatButton';


const styles = {
  page: {
    margin: '30px',
    'font-family': 'Roboto, sans-serif',
  },
  container: {
    display: 'flex',
    'justify-content': 'space-between',
    width: '50%'
  },
  card: {
    width: '30%',
  }
}
export default class Charts extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [ {sets: ['Jail'], size: 500}, {sets: ['Homeless'], size: 340}, {sets: ['Jail','Homeless'], size: 100}],
    };
  }

  render() {
    return (
      <div style={styles.page}>
        <h2>Charts</h2>
        <div>
          <Card style={styles.card}>
            <CardTitle title="Venn Diagram" titleStyle={{'font-size': 22}} />
            <Venn data={this.state.data} />
          </Card>
        </div>
      </div>
    )
  }
}
