import React from 'react'
import d3 from 'd3'
import DurationBarChart from './bar'
import Venn from './venn'
import TableList from './table'
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
  },
  card: {
    width: '100%',
  }
}
export default class Charts extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [ {sets: ['Jail'], size: 500}, {sets: ['Homeless'], size: 340}, {sets: ['Jail','Homeless'], size: 100}],
      table_data: [
                { ID: 12319, Name: 'Roy Batty', Source: ['Jail', 'Homeless'], Duration: 10 },
                { ID: 17144, Name: 'James Moriarty', Source: ['Jail', 'Homeless'], Duration: 18 },
                { ID: 12432, Name: 'Jason Smith', Source: 'Homeless', Duration: 1 },
                { ID: 19332, Name: 'H. H. Holmes', Source: 'Jail', Duration: 241 },
                { ID: 19032, Name: 'Jack Ripper', Source: 'Jail', Duration: 102 },
                { ID: 12143, Name: 'Lee Salminen', Source: 'Homeless', Duration: 43 },
                { ID: 12833, Name: 'John Doe', Source: ['Jail', 'Homeless'], Duration: 10 },
                { ID: 13833, Name: 'Jane Doe', Source: 'Homeless', Duration: 1 },
                { ID: 13932, Name: 'Evan Jackson', Source: ['Jail', 'Homeless'], Duration: 5 },
                { ID: 19982, Name: 'Liam Smith', Source: 'Homeless', Duration: 7 },
                { ID: 19932, Name: 'Griffin Smith', Source: 'Homeless', Duration: 3 },
      ]
    };
  }

  render() {
    return (
      <div style={styles.page}>
        <h2>Charts</h2>
        <div style={styles.container}>
          <Card style={styles.card}>
            <CardTitle title="Venn Diagram" titleStyle={{'font-size': 22}} />
            <Venn data={this.state.data} />
          </Card>
          <Card style={styles.card}>
            <CardTitle title="List" titleStyle={{'font-size': 22}} />
            <TableList data={this.state.table_data} />
          </Card>
          <Card style={styles.card}>
            <CardTitle title="Duration Bar Chart" titleStyle={{'font-size': 22}} />
            <DurationBarChart />
          </Card>
        </div>
      </div>
    )
  }
}
