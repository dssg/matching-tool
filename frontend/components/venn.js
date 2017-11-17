import React from 'react'
import d3 from 'd3'
import * as venn from 'venn.js'
import { updateTableData, getMatchingResults } from '../actions'
import { connect } from 'react-redux'

function mapStateToProps(state) {
  return {
    matchingResults: state.app.matchingResults,
    tableData: state.app.matchingResults.filteredData.tableData,
  }
}


function mapDispatchToProps(dispatch) {
  return {
    getUpdateTableData: (data, section) => {
      dispatch(updateTableData(data, section))
    },
    updateMatchingResults: (d) => {
      dispatch(getMatchingResults(d))
    },
  }
}

class Venn extends React.Component {
	constructor(props) {
		super(props)
    this.state = {
      allTableData: props.matchingResults.filteredData.tableData,
    }
	}

  componentDidMount() {
    this.props.updateMatchingResults("1")
    // console.log(this.props.matchingResults.filteredData.tableData)
    this.createVenn()
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.matchingResults.filters.startDate != nextProps.matchingResults.filters.startDate) {
      // console.log(nextProps.matchingResults.filteredData.tableData)
      this.setState({ allTableData: nextProps.matchingResults.filteredData.tableData})
    }
  }

  componentDidUpdate() {
    this.createVenn()
  }

  createVenn() {
    // console.log(this.state.allTableData)
    // console.log(this.props.tableData)
    const self = this
    const chart = venn.VennDiagram().width(320).height(270)
    const node = this.node
    const div = d3.select(node)
    var tooltip = d3.select(node).append("span").attr("class", "venntooltip")
    div.datum(self.props.data).call(chart)
    d3.selectAll(".venn-circle path").style("fill-opacity", .5)
    d3.selectAll(".venn-area path").style("fill-opacity", .5)
    d3.selectAll(".label").style("fill", "white")
                        .style("font-weight", "100")
                        .style("font-size", "14px")

    d3.selectAll(".venn-area")
      .on("mouseover", function(d, i) {
        const node = d3.select(this)
        node.select("path").style("fill-opacity", .8)
        node.select(".label").style("font-weight", "100")
                           .style("font-size", "20px")
        tooltip.style("opacity", .7)
        		 	 .style("left", (d3.event.pageX) + "px")
        		 	 .style("top", (d3.event.pageY - 28) + "px");
        tooltip.text(d.size + " people");
      })
      .on("mouseout", function(d, i) {
        const node = d3.select(this)
        node.select("path").style("fill-opacity", .5)
        node.select("text").style("font-weight", "100")
                           .style("font-size", "18px")
        tooltip.style("opacity", 0)
      })

    d3.selectAll(".venn-area")
      .on("click", function(d, i){
        self.props.getUpdateTableData(self.state.allTableData, d['sets'])
        tooltip.style("opacity", 0)

      })
  }

  render() {
  	return (
  		<g transform="translate(10, 30)" ref={node => this.node = node} />
  	)
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Venn)
