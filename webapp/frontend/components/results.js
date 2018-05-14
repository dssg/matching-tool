import ContentAdd from 'material-ui/svg-icons/content/add'
import DatePicker from 'material-ui/DatePicker'
import Drawer from 'material-ui/Drawer'
import DurationBarChart from './bar'
import FloatingActionButton from 'material-ui/FloatingActionButton'
import Loadable from 'react-loading-overlay'
import Header from './header'
import moment from 'moment'
import MenuItem from 'material-ui/MenuItem'
import NavigationClose from 'material-ui/svg-icons/navigation/close'
import RaisedButton from 'material-ui/RaisedButton'
import React from 'react'
import SelectField from 'material-ui/SelectField'
import DataTables from 'material-ui-datatables'
import Venn from './venn'
import { connect } from 'react-redux'
import { join, keys, map, merge, toPairs } from 'ramda'
import { getMatchingResults, updateControlledDate, updateTableSort, nextTablePage, prevTablePage, updateSetStatus, toggleBarFlag } from '../actions'
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
  summary: {
    "textAlign": "right",
    float:"right",
    marginRight: 7,
  },
  h5: {
    marginBottom: 2,
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
    marginTop: 0,
    padding: 8
  },
  table: {
    width: 'initial'
  },
  tableBody: {
    overflowX: 'auto'
  },
  tableColumn: {
    paddingLeft: '8px',
    paddingRight: '8x'
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
    filteredData: state.app.matchingResults.filteredData,
    vennDiagramData: state.app.matchingResults.vennDiagramData,
    jailCount: state.app.matchingResults.vennDiagramData[0]["size"],
    homelessCount: state.app.matchingResults.vennDiagramData[1]["size"],
    bothCount: state.app.matchingResults.vennDiagramData[2]["size"],
    totalCount: state.app.matchingResults.vennDiagramData[0]["size"]
      + state.app.matchingResults.vennDiagramData[1]["size"] - state.app.matchingResults.vennDiagramData[2]["size"],
    selectedJurisdictionSlug: state.app.selectedJurisdiction.slug,
    matchingIsLoading: state.app.matchingIsLoading,
    serverError: state.app.serverError,
    filters: state.app.matchingFilters,
    totalTableRows: state.app.matchingResults.totalTableRows,
    barFlag: state.app.barFlag
  }
}

function mapDispatchToProps(dispatch) {
  return {
    updateMatchingResults: (jurisdiction, matchingUrlParams) => {
      if(jurisdiction !== '') {
        dispatch(getMatchingResults(matchingUrlParams))
      } else {
        console.log('Short-circuiting matching results querying because no jurisdiction is selected yet')
      }
    },
    updateDates: (startDate, endDate) => {
      dispatch(updateControlledDate(startDate, endDate))
    },
    updateTableSort: (orderColumn, order) => {
      dispatch(updateTableSort(orderColumn, order))
    },
    nextPage: (event) => {
      dispatch(nextTablePage())
    },
    prevPage: (event) => {
      dispatch(prevTablePage())
    },
    handleUpdateSetStatus: (d) => {
      dispatch(updateSetStatus(d))
    },
    toggleBarFlag: () => {
      dispatch(toggleBarFlag())
    }
  }
}

export class Results extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: true,
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

  handleControlledDate = (event, date) => {
    const endDate = moment(date).format('YYYY-MM-DD')
    const startDate = moment(date).subtract(this.state.duration[0], this.state.duration[1]).format('YYYY-MM-DD')
    this.props.updateDates(startDate, endDate)
  }

  handleClickToggleChartAndList = () => {
    if (this.props.filters.setStatus == "Intersection") {
      this.props.handleUpdateSetStatus(["Jail"])
    }
    this.props.toggleBarFlag()
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
    const endDate = this.props.filters.endDate
    const startDate = moment(endDate).subtract(d[0], d[1]).format('YYYY-MM-DD')
    this.props.updateDates(startDate, endDate)
  }

  handleDownloadChart = () => {
    if (this.props.filters.setStatus == "Jail" | this.props.filters.setStatus == "All") {
      var id = "#jailbarchart"
    }
    else {
      var id = "#hmisbarchart"
    }
    html2canvas(document.querySelector(id)).then(canvas => {
      var dataURL = canvas.toDataURL()
      downloadURI(canvas.toDataURL(), "barchart.png")
    })
  }

  assembleURLParams = () => {
    const params = merge(this.props.filters, {jurisdiction: this.props.selectedJurisdictionSlug})
    return join('&', map(
      (key) => encodeURIComponent(key) + '=' + encodeURIComponent(params[key]),
      keys(params)
    ))
  }

  handleDownloadList = () => {
    const url = '/api/chart/download_list?' + this.assembleURLParams()
    downloadURI(url)
  }

  handleAll = () => {
    this.props.handleUpdateSetStatus(["All"])
  }

  intersectionPercentage = () => {
    var h = (this.props.bothCount / this.props.homelessCount).toFixed(3)*100
    var j = (this.props.bothCount / this.props.jailCount).toFixed(3)*100
    return (
      <span>
        <strong>{h}%</strong> of HMIS, <strong>{j}%</strong> of Jail
      </span>
    )
  }

  componentDidMount() {
    this.handleControlledDate('blah', new moment())
  }

  componentDidUpdate(prevProps) {
    if (this.props.filters != prevProps.filters || this.props.selectedJurisdictionSlug != prevProps.selectedJurisdictionSlug) {
      this.props.updateMatchingResults(
        this.props.selectedJurisdictionSlug,
        this.assembleURLParams()
      )
    }
  }

  renderTable() {
    const columns = map(
      function(k) { return {key: k, label: k, sortable: true, style: styles.tableColumn}; },
      keys(this.props.filteredData.tableData[0])
    )
    return (
      <div style={styles.container}>
        <Card style={styles.card_close}>
          <Loadable
            active={this.props.matchingIsLoading}
            color='#999999'
            spinner
            text='Loading records'
          >
            <DataTables
              tableBodyStyle={styles.tableBody}
              tableStyle={styles.table}
              columns={columns}
              data={this.props.filteredData.tableData}
              count={this.props.totalTableRows}
              rowSize={Number(this.props.filters.limit)}
              onNextPageClick={this.props.nextPage}
              onPreviousPageClick={this.props.prevPage}
              initialSort={{column: this.props.filters.orderColumn, order: this.props.filters.order}}
              onSortOrderChange={this.props.updateTableSort}
              page={1+(Number(this.props.filters.offset) / Number(this.props.filters.limit))}
              showRowSizeControls={false}
              showCheckboxes={false} />
          </Loadable>
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
            <CardTitle
              style={styles.cardTitle}
              title={"Homeless: number of shelter days - " + this.props.filters.startDate + " to " + this.props.filters.endDate}
              titleStyle={{'fontSize': 16, 'marginLeft': 10}} />
            <DurationBarChart
              data={this.props.filteredData.homelessDurationBarData}
              legendItemList={["0 day", "1 day", "2-9 days", "10-89 days", "90+ days"]} />
          </Card>
        </GridTile>
        <GridTile>
          <Card style={styles.bar_chart}>
            <CardTitle
              style={styles.cardTitle}
              title={"Homeless: number of contacts - " + this.props.filters.startDate + " to " + this.props.filters.endDate}
              titleStyle={{'fontSize': 16, 'marginLeft': 10}} />
            <DurationBarChart
              data={this.props.filteredData.homelessContactBarData}
              legendItemList={["1 contact", "2-9 contacts", "10-99 contacts", "100-499 contacts", "500+ contacts"]} />
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
            <CardTitle
              style={styles.cardTitle}
              title={"Jail: number of days - " + this.props.filters.startDate + " to " + this.props.filters.endDate}
              titleStyle={{'fontSize': 16, 'marginLeft': 10}} />
            <DurationBarChart data={this.props.filteredData.jailDurationBarData} />
          </Card>
        </GridTile>
        <GridTile>
          <Card style={styles.bar_chart}>
            <CardTitle
              style={styles.cardTitle}
              title={"Jail: number of contacts - " + this.props.filters.startDate + " to " + this.props.filters.endDate}
              titleStyle={{'fontSize': 16, 'marginLeft': 10}} />
            <DurationBarChart data={this.props.filteredData.jailContactBarData} />
          </Card>
        </GridTile>
      </GridList>
    )
  }

  renderBarChart() {
    if (this.props.filters.setStatus == "Jail" | this.props.filters.setStatus == "All") {
      return (
        <div style={styles.container}>
          {this.renderJailBarChart()}
        </div>
      )
    } else if (this.props.filters.setStatus == "HMIS") {
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
    if (this.props.serverError) {
      return (
        <div>
          <Header location={this.props.location} />
          <div style={styles.page}>
            Error: {this.props.serverError}
          </div>
        </div>
      )
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
            containerStyle={{height: 'calc(100% - 93px)', top: 48}}
            onRequestChange={(open) => this.setState({open})} >
            <div style={styles.container}>
              <Card style={styles.panel}>
                <CardTitle title="Control Panel" titleStyle={{'fontSize': 20, }} />
                <FloatingActionButton
                  onClick={this.handleClose}
                  mini={true}
                  secondary={true}
                  style={styles.floatingActionButtonClose} >
                  <NavigationClose />
                </FloatingActionButton>
                <div style={styles.datepicker}>
                  <h5 style={styles.h5}>End Date:
                    <DatePicker
                      defaultDate={new moment().toDate()}
                      maxDate={new moment().toDate()}
                      hintText="Pick a Date to go back"
                      autoOk={true}
                      onChange={this.handleControlledDate} />
                  </h5>
                  <h5 style={styles.h5}>Duration:</h5>
                  <h5 style={styles.h5}>
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
                    label={ this.props.barFlag ? "Show List of Results" : "Show Duration Chart"}
                    labelStyle={{fontSize: '10px',}}
                    style={styles.button}
                    primary={true}
                    onClick={this.handleClickToggleChartAndList} />
                  <RaisedButton
                    label="All"
                    style={{margin: 5}}
                    onClick={this.handleAll}
                    labelStyle={{fontSize: '10px',}} />
                </div>
                <Venn
                  data={this.props.vennDiagramData}
                  jail={this.props.jailCount}
                  homeless={this.props.homelessCount}
                  both={this.props.bothCount} />
              </Card>
            </div>
            <div style={styles.datepicker}>
              <RaisedButton
                label="Download Source HMIS"
                labelStyle={{fontSize: '10px',}}
                secondary={true}
                disabled={true}
                style={styles.button} />
              <RaisedButton
                label="Download Source Jail"
                labelStyle={{fontSize: '10px',}}
                secondary={true}
                disabled={true}
                style={styles.button} />
            </div>
            <div style={styles.datepicker}>
              <RaisedButton
                label={ this.props.barFlag ? "Download Charts" : "Download List" }
                labelStyle={{fontSize: '10px',}}
                secondary={true}
                onClick={ this.props.barFlag? this.handleDownloadChart : this.handleDownloadList}
                style={styles.button} />
            </div>
          </Drawer>
        </div>
        <div style={contentStyle}>
          <div>
            <h4 style={styles.h4}>Results - {this.props.filters.startDate} through {this.props.filters.endDate} - {this.props.filters.setStatus}</h4>
            <h5 style={styles.summary}>
                Total: <strong>{this.props.totalCount}</strong>&nbsp;
                Jail: <strong>{this.props.jailCount}</strong>&nbsp;
                HMIS: <strong>{this.props.homelessCount}</strong>&nbsp;
                Intersection: <strong>{this.props.bothCount}</strong> ({this.intersectionPercentage()})&nbsp;
            </h5>
            <hr style={styles.hr}/>
          </div>
          { this.props.barFlag ? this.renderBarChart() : this.renderTable() }
        </div>
      </div>
    )
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Results)
