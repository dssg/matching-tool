import React from 'react'
import { event, select, selectAll } from 'd3-selection'
import * as venn from 'venn.js'
import { updateSetStatus } from '../actions'
import { connect } from 'react-redux'
import RaisedButton from 'material-ui/RaisedButton'
import { filter } from 'ramda'
import ReactTooltip from 'react-tooltip'

function mapStateToProps(state) {
  return {
    tableData: state.app.matchingResults.filteredData.tableData,
    filters: state.app.matchingFilters,
    barFlag: state.app.barFlag
  }
}


function mapDispatchToProps(dispatch) {
  return {
    handleUpdateSetStatus: (d) => {
      dispatch(updateSetStatus(d))
    },
  }
}

class Venn extends React.Component {
	constructor(props) {
		super(props)
    this.state = {
      allTableData: props.tableData,
    }
	}

  componentDidMount() {
    this.createVenn()
    ReactTooltip.rebuild()
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.filters.startDate != nextProps.filters.startDate) {
      this.setState({ allTableData: nextProps.tableData})
    }
  }

  componentDidUpdate() {
    this.createVenn()
    ReactTooltip.rebuild()
  }

  filterVenn(data) {
    var isSizeNotZero = x => x.size !==0
    const filtered_venndata = filter(isSizeNotZero, data)
    if (filtered_venndata.length == 0) {
      return [{sets: [''], size: null}, {sets: [''], size: null}, {sets: [''], size: null}]
    } else {
      return filtered_venndata
    }
  }

  createVenn() {
    const self = this
    const chart = venn.VennDiagram().width(0.24*window.innerWidth)
    const node = this.node
    const div = select(node)
    const venndata = self.filterVenn(self.props.data)
    if (venndata.length == 1) {
      self.props.handleUpdateSetStatus(venndata[0]['sets'])
    }
    div.datum(venndata).call(chart)
    selectAll(".venn-circle path").style("fill-opacity", .65)
    selectAll(".venn-area path").style("fill-opacity", .65)
    selectAll(".label").style("fill", "white")
                          .style("font-weight", "100")
                          .style("font-size", "14px")

    selectAll(".venn-area").attr("data-tip", "true")
                              .attr("data-for", function(d, i) {
                                if (d['sets'].length == 2) {
                                  return "intersection"
                                } else if ("Jail" == d['sets'][0]) {
                                  return "jail"
                                } else if ("Homeless" == d['sets'][0]) {
                                  return "homeless"}
                                })

    selectAll(".venn-area path")
        .style("fill", function(d, i){
          if ("Jail" == d['sets'][0]) {
            return "#1f77b4"
          } else if ("Homeless" == d['sets'][0]) {
            return "#ff7f0e"
          }
      })

    selectAll(".venn-area")
      .on("mouseover", function(d, i) {
        const node = select(this)
        if (!self.props.barFlag || d['sets'].length == 1) {
          node.select("path").style("fill-opacity", .8)
                           .style("stroke-width", 3)
                           .style("stroke", "red")
        }

        node.select(".label").style("font-weight", "100")
                             .style("font-size", "20px")
      })
      .on("mouseout", function(d, i) {
        const node = select(this)
        node.select("path").style("fill-opacity", .65)
                           .style("stroke-width", 0)
        node.select("text").style("font-weight", "100")
                           .style("font-size", "14px")
      })

    selectAll(".venn-area")
      .on("click", function(d, i){
        const node = select(this)
        if (!self.props.barFlag || d['sets'].length == 1) {
          self.props.handleUpdateSetStatus(d['sets'])
        }
      })
  }

  render() {
  	return (
      <div style={{marginLeft: 10}}>
        <ReactTooltip id="jail">
          <p>{this.props.jail} people</p>
        </ReactTooltip>
        <ReactTooltip id="homeless">
          <p>{this.props.homeless} people</p>
        </ReactTooltip>
        <ReactTooltip id="intersection">
          <p>{this.props.both} people</p>
        </ReactTooltip>
        <g ref={node => this.node = node} />
        <p> * Left circle is always larger or equal</p>
      </div>
  	)
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Venn)
