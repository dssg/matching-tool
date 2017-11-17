import ContentAdd from 'material-ui/svg-icons/content/add'
import DatePicker from 'material-ui/DatePicker'
import Drawer from 'material-ui/Drawer'
import DurationBarChart from './bar'
import FloatingActionButton from 'material-ui/FloatingActionButton'
import Header from './header'
import MenuItem from 'material-ui/MenuItem'
import NavigationClose from 'material-ui/svg-icons/navigation/close'
import RaisedButton from 'material-ui/RaisedButton'
import React from 'react'
import SelectField from 'material-ui/SelectField'
import TableList from './table'
import Venn from './venn'
import { connect } from 'react-redux'
import { getMatchingResults, updateControlledDate, updateDuration } from '../actions'
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card'

const styles = {
  hr: {
    clear: "both",
    margin: 0
  },
  h4: {
    "text-align": "left",
    float:"left",
    "margin-top": 6,
    marginLeft: 60,
  },
  h5: {
    "text-align": "right",
    float:"right",
    marginRight: 7
  },
  page: {
    margin: '5px',
    'font-family': 'Roboto, sans-serif',
  },
  container: {
    display: 'flex',
    'justify-content': 'space-between',
  },
  datepicker: {
    marginLeft: 15,
  },
  panel: {
    width: '100%',
    marginLeft: 5
  },
  card: {
    width: '50%',
    expanded: true,
  },
  card_close: {
    width: '100%',
    expanded: true,
    marginLeft: 60,
    marginRight: 7
  },
  bar_chart_jail: {
    width: '50%',
    marginLeft: 60,
  },
  bar_chart_homeless: {
    width: '50%',
    marginRight: 7
  },
  button: {
    margin: '12',
  },
  floatingActionButtonAdd: {
    position: 'absolute',
    top: '50%',
    marginLeft: 5
  },
  floatingActionButtonClose: {
    position: 'absolute',
    top: '2%',
    marginLeft: '85%'
  },
}

function mapStateToProps(state) {
  return {
    matchingResults: state.app.matchingResults,
    controlledDate: state.app.matchingResults.filters.controlledDate,
    duration: state.app.matchingResults.filters.duration,
    startDate: state.app.matchingResults.filters.startDate,
    endDate: state.app.matchingResults.filters.endDate,
    jailCount: state.app.matchingResults.vennDiagramData[0]["size"],
    homelessCount: state.app.matchingResults.vennDiagramData[1]["size"],
    bothCount: state.app.matchingResults.vennDiagramData[2]["size"],
    totalCount: state.app.matchingResults.vennDiagramData[0]["size"]
      + state.app.matchingResults.vennDiagramData[1]["size"] - state.app.matchingResults.vennDiagramData[2]["size"],
  }
}

function mapDispatchToProps(dispatch) {
  return {
    updateMatchingResults: (d) => {
      dispatch(getMatchingResults(d))
    },
    handleControlledDate: (event, date) => {
      dispatch(updateControlledDate(date))
    },
    handleDurationChange: (event, index, value) => {
      dispatch(updateDuration(value))
    },
  }
}

class Results extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: true,
      barFlag: false,
      showHomelessDurationChart: false,
    }
  }

  handleToggle = () => {
    this.setState({
      open: !this.state.open
    })
  }

  handleClose = () => {
    this.setState({
      open: false,
    })
  }

  handleSearch = () => {
    this.props.updateMatchingResults("2")
  }

  handleClick = () => {
    this.setState({barFlag: !this.state.barFlag})
  }

  componentDidMount() {
    this.props.updateMatchingResults("1")
  }

  renderTable() {
    return (
      <div style={styles.container}>
        <Card style={styles.card_close}>
          <TableList data={this.props.matchingResults.filteredData.tableData} />
        </Card>
      </div>
    )
  }

  renderHomelessBarChart() {
    return (
      <Card style={styles.bar_chart_homeless}>
        <CardTitle title="Homeless Duration Bar Chart" titleStyle={{'font-size': 20}} />
          <DurationBarChart data={this.props.matchingResults.filteredData.homelessBarData} />
      </Card>
    )
  }

  renderBarChart() {
    return (
      <div style={styles.container}>
        <Card style={styles.bar_chart_jail}>
          <CardTitle title="Jail Duration Bar Chart" titleStyle={{'font-size': 20}} />
            <DurationBarChart data={this.props.matchingResults.filteredData.jailBarData} />
        </Card>
        { this.state.showHomelessDurationChart ? renderHomelessBarChart() : null}
      </div>
    )
  }

  render() {
    console.log(this.props.matchingResults.filteredData.tableData)
    const contentStyle = {  transition: 'margin-left 300ms cubic-bezier(0.23, 1, 0.32, 1)' }
    if (this.state.open) {
      contentStyle.marginLeft = '25%'
    }
    return (
      <div>
        <Header location={this.props.location} />
        <div style={styles.page}>
          <FloatingActionButton
            style={styles.floatingActionButtonAdd}
            mini={true}
            onClick={this.handleToggle} >
            <ContentAdd />
          </FloatingActionButton>
          <Drawer
            docked={true}
            width={'25%'}
            open={this.state.open}
            containerStyle={{height: 'calc(100% - 48px)', top: 48}}
            onRequestChange={(open) => this.setState({open})} >
            <div style={styles.container}>
              <Card style={styles.panel}>
                <CardTitle title="Control Panel" titleStyle={{'font-size': 20}} />
                <FloatingActionButton
                  onClick={this.handleClose}
                  mini={true}
                  secondary={true}
                  style={styles.floatingActionButtonClose} >
                  <NavigationClose />
                </FloatingActionButton>
                <div style={styles.datepicker}>
                  <h5>End Date:
                    <DatePicker
                      hintText="Pick the data to go back"
                      value={this.props.controlledDate}
                      onChange={this.props.handleControlledDate} />
                  </h5>
                  <h5>Duration:</h5>
                  <h5>
                    <SelectField
                      value={this.props.duration}
                      onChange={this.props.handleDurationChange}
                      maxHeight={200} >
                      <MenuItem value={30} key={1} primaryText={`1 Month`} />
                      <MenuItem value={90} key={2} primaryText={`3 Months`} />
                      <MenuItem value={365} key={3} primaryText={`1 Year`} />
                    </SelectField>
                  </h5>
                  <RaisedButton
                    label="Search"
                    onClick={this.handleSearch}/>
                  <RaisedButton
                    label={ this.state.barFlag ? "Show List of Results" : "Show Duration Chart"}
                    primary={true}
                    onClick={this.handleClick} />
                </div>
                <Venn
                  data={this.props.matchingResults.vennDiagramData}
                  local_table_data={this.props.matchingResults.filteredData.tableData}/>
              </Card>
            </div>
            <a href={ this.state.barFlag ? "/api/chart/download/chart" : "/api/chart/download/list" }>
              <RaisedButton
                label={ this.state.barFlag ? "Download Charts" : "Download List" }
                secondary={true}
                style={styles.button} />
            </a>
          </Drawer>
        </div>
        <div style={contentStyle}>
          <div>
            <h4 style={styles.h4}>Results - {this.props.startDate} through {this.props.endDate}</h4>
            <h5 style={styles.h5}>
                Total: <strong>{this.props.totalCount}</strong>&nbsp;
                Jail: <strong>{this.props.jailCount}</strong>&nbsp;
                Homeless: <strong>{this.props.homelessCount}</strong>&nbsp;
                Intersection: <strong>{this.props.bothCount}</strong>&nbsp;
            </h5>
            <hr style={styles.hr}/>
          </div>
          { this.state.barFlag ? this.renderBarChart(): this.renderTable() }
        </div>
      </div>
    )
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Results)
