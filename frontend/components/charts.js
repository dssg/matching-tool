import React from 'react'
import d3 from 'd3'
import DurationBarChart from './bar'
import Venn from './venn'
import TableList from './table'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import RaisedButton from 'material-ui/RaisedButton';
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
  venn: {
    width: '60%',
  },
  card: {
    width: '120%',
  },
  bar_chart: {
    width: '70%',
  },
  list: {
    'text-align': 'center',
  },
  button: {
    margin: '12',
  }
}
export default class Charts extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [ {sets: ['Jail'], size: 500}, {sets: ['Homeless'], size: 340}, {sets: ['Jail','Homeless'], size: 100}],
      table_data: [
                { ID: 12319,
                  Name: 'Roy Batty',
                  Source: ['Jail', 'Homeless'],
                  'Total Duration': 10,
                  'Total Counts': 5,
                  '# of Jail Days': 8,
                  '# of Jail Counts': 3,
                  '# of Homeless Days': 2,
                  '# of Homeless Counts': 2 },
                { ID: 17144,
                  Name: 'James Moriarty',
                  Source: ['Jail', 'Homeless'],
                  'Total Duration': 18,
                  'Total Counts': 8,
                  '# of Jail Days': 16,
                  '# of Jail Counts': 5,
                  '# of Homeless Days': 2,
                  '# of Homeless Counts': 3 },
                { ID: 12432,
                  Name: 'Jason Smith',
                  Source: 'Homeless',
                  'Total Duration': 1,
                  'Total Counts': 1,
                  '# of Jail Days': 0,
                  '# of Jail Counts': 0,
                  '# of Homeless Days': 1,
                  '# of Homeless Counts': 2 },
                { ID: 19332,
                  Name: 'H. H. Holmes',
                  Source: 'Jail',
                  'Total Duration': 241,
                  'Total Counts': 1,
                  '# of Jail Days': 241,
                  '# of Jail Counts': 1,
                  '# of Homeless Days': 0,
                  '# of Homeless Counts': 0 },
                { ID: 19032,
                  Name: 'Jack Ripper',
                  Source: 'Jail',
                  'Total Duration': 102,
                  'Total Counts': 2,
                  '# of Jail Days': 102,
                  '# of Jail Counts': 2,
                  '# of Homeless Days': 0,
                  '# of Homeless Counts': 0 },
                { ID: 12143,
                  Name: 'Lee Salminen',
                  Source: 'Homeless',
                  'Total Duration': 43,
                  'Total Counts': 5,
                  '# of Jail Days': 0,
                  '# of Jail Counts': 0,
                  '# of Homeless Days': 43,
                  '# of Homeless Counts': 5 },
                { ID: 12833,
                  Name: 'John Doe',
                  Source: ['Jail', 'Homeless'],
                  'Total Duration': 10,
                  'Total Counts': 3,
                  '# of Jail Days': 2,
                  '# of Jail Counts': 1,
                  '# of Homeless Days': 8,
                  '# of Homeless Counts': 2 },
                { ID: 13833,
                  Name: 'Jane Doe',
                  Source: 'Homeless',
                  'Total Duration': 2,
                  'Total Counts': 2,
                  '# of Jail Days': 0,
                  '# of Jail Counts': 0,
                  '# of Homeless Days': 2,
                  '# of Homeless Counts': 2 },
                { ID: 13932,
                  Name: 'Evan Jackson',
                  Source: ['Jail', 'Homeless'],
                  'Total Duration': 5,
                  'Total Counts': 2,
                  '# of Jail Days': 1,
                  '# of Jail Counts': 1,
                  '# of Homeless Days': 4,
                  '# of Homeless Counts': 1 },
                { ID: 19982,
                  Name: 'Liam Smith',
                  Source: 'Homeless',
                  'Total Duration': 7,
                  'Total Counts': 3,
                  '# of Jail Days': 0,
                  '# of Jail Counts': 0,
                  '# of Homeless Days': 7,
                  '# of Homeless Counts': 3 },
                { ID: 19932,
                  Name: 'Griffin Smith',
                  Source: 'Homeless',
                  'Total Duration': 3,
                  'Total Counts': 2,
                  '# of Jail Days': 0,
                  '# of Jail Counts': 0,
                  '# of Homeless Days': 3,
                  '# of Homeless Counts': 2 },
      ],
      bar_data: [
        [{x: 'Jail', y: 40}, {x: 'Homeless', y: 20}, {x: 'Jail & Homeless', y: 30}],
        [{x: 'Jail', y: 20}, {x: 'Homeless', y: 15}, {x: 'Jail & Homeless', y: 30}],
        [{x: 'Jail', y: 30}, {x: 'Homeless', y: 25}, {x: 'Jail & Homeless', y: 20}],
        [{x: 'Jail', y: 5}, {x: 'Homeless', y: 30}, {x: 'Jail & Homeless', y: 10}],
        [{x: 'Jail', y: 5}, {x: 'Homeless', y: 10}, {x: 'Jail & Homeless', y: 10}],
      ]
    }
  }

  render() {
    return (
      <div style={styles.page}>
        <h2>Charts - 7/1/2017 through 7/31/2017</h2>
        <div style={styles.container}>
          <Card style={styles.venn}>
            <CardTitle title="Venn Diagram" titleStyle={{'font-size': 22}} />
            <Venn data={this.state.data} />
          </Card>
          <Card style={styles.card}>
            <CardTitle title="List" titleStyle={{'font-size': 22}} />
            <div style={styles.list}>
              <h5>Total: <strong>740</strong>&nbsp;
                Jail: <strong>500</strong>&nbsp;
                Homeless: <strong>340</strong>&nbsp;
                Intersection: <strong>100</strong>&nbsp;
            </h5>
            </div>
            <TableList data={this.state.table_data} />
          </Card>
          <Card style={styles.bar_chart}>
            <CardTitle title="Duration Bar Chart" titleStyle={{'font-size': 22}} />
            <DurationBarChart data={this.state.bar_data} />
          </Card>
        </div>
        <RaisedButton label="Download List" secondary={true} style={styles.button} />
        <RaisedButton label="Download Charts" secondary={true} style={styles.button} />
      </div>
    )
  }
}
