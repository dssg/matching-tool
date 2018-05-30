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
import { getMatchingResults, setAppState, nextTablePage, prevTablePage, updateSetStatus, toggleBarFlag } from '../actions'
import { Card, CardTitle } from 'material-ui/Card'
import {GridList, GridTile} from 'material-ui/GridList';
import html2canvas from 'html2canvas'
import SourceDownloader from './source-downloader'

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
    marginBottom: 10
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
    marginTop: 5,
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
    updateStartDate: (startDate) => {
      dispatch(setAppState('matchingFilters.startDate', startDate))
    },
    updateEndDate: (endDate) => {
      dispatch(setAppState('matchingFilters.endDate', endDate))
    },
    updateTableSort: (orderColumn, order) => {
      dispatch(setAppState('matchingFilters.order', order))
      dispatch(setAppState('matchingFilters.orderColumn', orderColumn))
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

  handleStartDate = (event, date) => {
    const startDate = moment(date).format('YYYY-MM-DD')
    this.props.updateStartDate(startDate)
  }

  handleEndDate = (event, date) => {
    const endDate = moment(date).format('YYYY-MM-DD')
    this.props.updateEndDate(endDate)
  }

  handleClickToggleChartAndList = () => {
    if (this.props.filters.setStatus == "Intersection") {
      this.props.handleUpdateSetStatus(["Jail"])
    }
    this.props.toggleBarFlag()
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
    var h = (100*this.props.bothCount / this.props.homelessCount).toPrecision(2)
    var j = (100*this.props.bothCount / this.props.jailCount).toPrecision(2)
    return (
      <span>
        <strong>{h}%</strong> of HMIS, <strong>{j}%</strong> of Jail
      </span>
    )
  }

  componentDidMount() {
    this.handleEndDate('blah', new moment())
    this.handleStartDate('blah', new moment().subtract(1, 'year'))

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
            <DurationBarChart data={this.props.filteredData.homelessDurationBarData} />
          </Card>
        </GridTile>
        <GridTile>
          <Card style={styles.bar_chart}>
            <CardTitle
              style={styles.cardTitle}
              title={"Homeless: number of contacts - " + this.props.filters.startDate + " to " + this.props.filters.endDate}
              titleStyle={{'fontSize': 16, 'marginLeft': 10}} />
            <DurationBarChart data={this.props.filteredData.homelessContactBarData} />
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
                  <h5 style={styles.h5}>Start Date:
                    <DatePicker
                      defaultDate={new moment().subtract(1, 'year').toDate()}
                      maxDate={new moment().toDate()}
                      hintText="Pick the Start Date"
                      onChange={this.handleStartDate} />
                  </h5>
                  <h5 style={styles.h5}>End Date:
                    <DatePicker
                      defaultDate={new moment().toDate()}
                      maxDate={new moment().toDate()}
                      hintText="Pick the End Date"
                      onChange={this.handleEndDate} />
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
                label={ this.props.barFlag ? "Download Duration Charts" : "Download List of Results" }
                labelStyle={{fontSize: '10px',}}
                secondary={true}
                onClick={ this.props.barFlag? this.handleDownloadChart : this.handleDownloadList}
                style={styles.button} />
            </div>
            <div style={styles.datepicker}>
              <SourceDownloader />
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
