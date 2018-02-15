import ContentAdd from 'material-ui/svg-icons/content/add'
import DatePicker from 'material-ui/DatePicker'
import Drawer from 'material-ui/Drawer'
import DurationBarChart from './bar'
import FloatingActionButton from 'material-ui/FloatingActionButton'
import Header from './header'
import moment from 'moment'
import MenuItem from 'material-ui/MenuItem'
import NavigationClose from 'material-ui/svg-icons/navigation/close'
import RaisedButton from 'material-ui/RaisedButton'
import React from 'react'
import SelectField from 'material-ui/SelectField'
import TableList from './table'
import Venn from './venn'
import { connect } from 'react-redux'
import { getMatchingResults, updateControlledDate } from '../actions'
import { Card, CardTitle } from 'material-ui/Card'
import {GridList, GridTile} from 'material-ui/GridList';
import html2canvas from 'html2canvas'

const styles = {
  hr: {
    clear: "both",
    margin: 0
  },
  h4: {
    "textAlign": "left",
    float:"left",
    "marginTop": 6,
    marginLeft: 60,
  },
  h5: {
    "textAlign": "right",
    float:"right",
    marginRight: 7
  },
  page: {
    margin: '5px',
    'fontFamily': 'Roboto, sans-serif',
  },
  container: {
    display: 'flex',
    'justifyContent': 'spaceBetween',
  },
  datepicker: {
    marginLeft: 15,
  },
  panel: {
    width: '105%',
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
    marginRight: 7,
    overflow: 'scroll',
  },
  bar_chart: {
    width: '100%',
    height: '100%',
    marginLeft: 60,
  },
  button: {
    margin: 5,
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
  gridList: {
    width: '100%',
    overflowY: 'auto',
  },
  cardTitle: {
    marginTop: 1
  }
}

function downloadURI(uri, name) {
    var link = document.createElement("a");

    link.download = name;
    link.href = uri;
    document.body.appendChild(link);
    link.click();
}

function mapStateToProps(state) {
  return {
    matchingResults: state.app.matchingResults,
    controlledDate: state.app.matchingResults.filters.controlledDate,
    startDate: state.app.matchingResults.filters.startDate,
    endDate: state.app.matchingResults.filters.endDate,
    jailCount: state.app.matchingResults.vennDiagramData[0]["size"],
    homelessCount: state.app.matchingResults.vennDiagramData[1]["size"],
    bothCount: state.app.matchingResults.vennDiagramData[2]["size"],
    totalCount: state.app.matchingResults.vennDiagramData[0]["size"]
      + state.app.matchingResults.vennDiagramData[1]["size"] - state.app.matchingResults.vennDiagramData[2]["size"],
    setStatus: state.app.matchingResults.filters.setStatus,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    updateMatchingResults: (start, end) => {
      dispatch(getMatchingResults(start, end))
    },
    handleControlledDate: (event, date) => {
      dispatch(updateControlledDate(date))
    },
  }
}

class Results extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: true,
      barFlag: false,
      flagJailBar: true,
      duration: [1, "year", 4]
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
    var date = moment(this.props.controlledDate).format('YYYY-MM-DD')
    var newdate = moment(date).subtract(this.state.duration[0], this.state.duration[1]).format('YYYY-MM-DD')
    this.props.updateMatchingResults(newdate, date)
  }

  handleClick = () => {
    this.setState({barFlag: !this.state.barFlag})
  }

  handleDurationChange = (event, index, value) => {
    if (value == 1) {
      var d = [1, "month", value]
    }
    else if (value == 2) {
      var d = [3, "months", value]
    }
    else if (value == 3) {
      var d = [6, "months", value]
    }
    else if (value == 4) {
      var d = [1, "year", value]
    }
    else if (value == 5) {
      var d = [2, "years", value]
    }
    this.setState({duration: d})
  }

  handleDownloadChart = () => {
    if (this.props.setStatus == "Jail" | this.props.setStatus == "All") {
      var id = "#jailbarchart"
    }
    else {
      var id = "#hmisbarchart"
    }
    html2canvas(document.querySelector(id)).then(canvas => {
    var dataURL = canvas.toDataURL()
    downloadURI(canvas.toDataURL(), "barchart.png");
    });
  }

  intersectionPercentage = () => {
    var h = Math.floor((this.props.bothCount / this.props.homelessCount)*100)
    var j = Math.floor((this.props.bothCount / this.props.jailCount)*100)
    return (
      <span>
        <strong>{h}%</strong> of HMIS, <strong>{j}%</strong> of Jail
      </span>
    )
  }

  componentDidMount() {
    var today = new moment().format("YYYY-MM-DD")
    var oneYearAgo = moment(today).subtract(1, "year").format("YYYY-MM-DD")
    this.props.updateMatchingResults(oneYearAgo, today)
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
      <GridList
        cellHeight='auto'
        cols={1}
        style={styles.gridList}
        id='hmisbarchart'>
        <GridTile>
          <Card  style={styles.bar_chart}>
            <CardTitle style={styles.cardTitle} title="Homeless Duration Bar Chart" titleStyle={{'fontSize': 18}} />
            <DurationBarChart
              data={this.props.matchingResults.filteredData.homelessDurationBarData}
              legendItemList={["0 day", "1 day", "2-9 days", "10-89 days", "90+ days"]} />
          </Card>
        </GridTile>
        <GridTile>
          <Card style={styles.bar_chart}>
            <CardTitle style={styles.cardTitle} title="Homeless # of Contact Bar Chart" titleStyle={{'fontSize': 18}} />
            <DurationBarChart
              data={this.props.matchingResults.filteredData.homelessContactBarData}
              legendItemList={["1 contacts", "2-9 contacts", "10-99 contacts", "100-499 contacts", "500+ contacts"]} />
          </Card>
        </GridTile>
      </GridList>
    )
  }

  renderJailBarChart() {
    return (
      <GridList
        cellHeight='auto'
        cols={1}
        style={styles.gridList}
        id='jailbarchart'>
        <GridTile>
          <Card style={styles.bar_chart}>
            <CardTitle style={styles.cardTitle} title="Jail Duration Bar Chart" titleStyle={{'fontSize': 18}} />
            <DurationBarChart
              data={this.props.matchingResults.filteredData.jailDurationBarData}
              legendItemList={["0 day", "1 day", "2-9 days", "10-89 days", "90+ days"]} />
          </Card>
        </GridTile>
        <GridTile>
          <Card style={styles.bar_chart}>
            <CardTitle style={styles.cardTitle} title="Jail # of Contact Bar Chart" titleStyle={{'fontSize': 18}} />
            <DurationBarChart
              data={this.props.matchingResults.filteredData.jailContactBarData}
              legendItemList={["1 contacts", "2-9 contacts", "10-99 contacts", "100-499 contacts", "500+ contacts"]} />
          </Card>
        </GridTile>
      </GridList>
    )
  }

  renderBarChart() {
    if (this.props.setStatus == "Jail" | this.props.setStatus == "All") {
      return (
        <div style={styles.container}>
          {this.renderJailBarChart()}
        </div>
      )
    } else if (this.props.setStatus == "HMIS") {
      return (
        <div style={styles.container}>
          {this.renderHomelessBarChart()}
        </div>
      )
    } else {
      if (this.state.flagJailBar) {
        return (
          <div style={styles.container}>
            {this.renderJailBarChart()}
          </div>
        )
      } else {
        return (
          <div style={styles.container}>
            {this.renderHomelessBarChart()}
          </div>
        )
      }
    }
  }

  render() {
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
                <CardTitle title="Control Panel" titleStyle={{'fontSize': 20}} />
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
                      onChange={this.props.handleControlledDate} />
                  </h5>
                  <h5>Duration:</h5>
                  <h5>
                    <SelectField
                      value={this.state.duration[2]}
                      onChange={this.handleDurationChange}
                      maxHeight={200} >
                      <MenuItem value={1} key={1} primaryText={`1 Month`} />
                      <MenuItem value={2} key={2} primaryText={`3 Months`} />
                      <MenuItem value={3} key={3} primaryText={`6 Months`} />
                      <MenuItem value={4} key={4} primaryText={`1 Year`} />
                      <MenuItem value={5} key={5} primaryText={`2 Years`} />
                    </SelectField>
                  </h5>
                  <RaisedButton
                    label="Search"
                    labelStyle={{fontSize: '10px',}}
                    style={styles.button}
                    onClick={this.handleSearch}/>
                  <RaisedButton
                    label={ this.state.barFlag ? "Show List of Results" : "Show Duration Chart"}
                    labelStyle={{fontSize: '10px',}}
                    style={styles.button}
                    primary={true}
                    onClick={this.handleClick} />
                </div>
                <Venn
                  data={this.props.matchingResults.vennDiagramData}
                  local_table_data={this.props.matchingResults.filteredData.tableData}/>
              </Card>
            </div>
            <div style={styles.datepicker}>
              <RaisedButton
                label="Download Source HMIS"
                labelStyle={{fontSize: '10px',}}
                secondary={true}
                style={styles.button} />
              <RaisedButton
                label="Download Source Jail"
                labelStyle={{fontSize: '10px',}}
                secondary={true}
                style={styles.button} />
            </div>
              <div style={styles.datepicker}>
                <RaisedButton
                  label={ this.state.barFlag ? "Download Charts" : "Download List" }
                  labelStyle={{fontSize: '10px',}}
                  secondary={true}
                  onClick={this.handleDownloadChart}
                  style={styles.button} />
              </div>
          </Drawer>
        </div>
        <div style={contentStyle}>
          <div>
            <h4 style={styles.h4}>Results - {this.props.startDate} through {this.props.endDate} - {this.props.setStatus}</h4>
            <h5 style={styles.h5}>
                Total: <strong>{this.props.totalCount}</strong>&nbsp;
                Jail: <strong>{this.props.jailCount}</strong>&nbsp;
                Homeless: <strong>{this.props.homelessCount}</strong>&nbsp;
                Intersection: <strong>{this.props.bothCount}</strong> ({this.intersectionPercentage()})&nbsp;
            </h5>
            <hr style={styles.hr}/>
          </div>
          { this.state.barFlag ? this.renderBarChart() : this.renderTable() }
        </div>
      </div>
    )
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Results)
