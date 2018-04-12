import React from 'react'
import d3 from 'd3'
import * as venn from 'venn.js'
import { updateSetStatus } from '../actions'
import { connect } from 'react-redux'
import RaisedButton from 'material-ui/RaisedButton'
import { filter } from 'ramda'
import ReactTooltip from 'react-tooltip'

function mapStateToProps(state) {
  return {
    tableData: state.app.matchingResults.filteredData.tableData,
    filters: state.app.matchingFilters
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

  createVenn() {
    const self = this
    const chart = venn.VennDiagram().width(340).height(250)
    const node = this.node
    const div = d3.select(node)
    var isSizeNotZero = x => x.size !== 0
    const venndata = filter(isSizeNotZero, self.props.data)
    div.datum(venndata).call(chart)
    d3.selectAll(".venn-circle path").style("fill-opacity", .65)
    d3.selectAll(".venn-area path").style("fill-opacity", .65)
    d3.selectAll(".label").style("fill", "white")
                          .style("font-weight", "100")
                          .style("font-size", "14px")

    d3.selectAll(".venn-area").attr("data-tip", "true")
                              .attr("data-for", function(d, i) {
                                if (d['sets'].length == 2) {
                                  return "intersection"
                                } else if ("Jail" == d['sets'][0]) {
                                  return "jail";
                                } else if ("Homeless" == d['sets'][0]) {
                                  return "homeless";
                              }
    })

    d3.selectAll(".venn-area")
      .on("mouseover", function(d, i) {
        const node = d3.select(this)
        node.select("path").style("fill-opacity", .8)
                           .style("stroke-width", 3)
                           .style("stroke", "red")

        node.select(".label").style("font-weight", "100")
                             .style("font-size", "20px")
      })
      .on("mouseout", function(d, i) {
        const node = d3.select(this)
        node.select("path").style("fill-opacity", .65)
                           .style("stroke-width", 0)
        node.select("text").style("font-weight", "100")
                           .style("font-size", "14px")
      })

    d3.selectAll(".venn-area")
      .on("click", function(d, i){
        const node = d3.select(this)
        self.props.handleUpdateSetStatus(d['sets'])
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
