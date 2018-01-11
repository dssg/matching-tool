import React from 'react'
import d3 from 'd3'
import * as venn from 'venn.js'
import { updateTableData, getMatchingResults, updateSetStatus } from '../actions'
import { connect } from 'react-redux'
import RaisedButton from 'material-ui/RaisedButton'


function mapStateToProps(state) {
  return {
    matchingResults: state.app.matchingResults,
    tableData: state.app.matchingResults.filteredData.tableData,
  }
}


function mapDispatchToProps(dispatch) {
  return {
    handleUpdateTableData: (data, section) => {
      dispatch(updateTableData(data, section))
    },
    updateMatchingResults: (d) => {
      dispatch(getMatchingResults(d))
    },
    handleUpdateSetStatus: (d) => {
      dispatch(updateSetStatus(d))
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

  handleReset = () => {
    this.props.handleUpdateTableData(this.state.allTableData, "All")
    this.props.handleUpdateSetStatus(["All"])
  }

  componentDidMount() {
    this.props.updateMatchingResults("1")
    this.createVenn()
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.matchingResults.filters.startDate != nextProps.matchingResults.filters.startDate) {
      this.setState({ allTableData: nextProps.matchingResults.filteredData.tableData})
    }
  }

  componentDidUpdate() {
    this.createVenn()
  }

  createVenn() {
    const self = this
    const chart = venn.VennDiagram().width(320).height(270)
    const node = this.node
    const div = d3.select(node)

    var tooltip = d3.select(node).append("div").attr("class", "venntooltip")
    div.datum(self.props.data).call(chart)
    d3.selectAll(".venn-circle path").style("fill-opacity", .65)
    d3.selectAll(".venn-area path").style("fill-opacity", .65)
    d3.selectAll(".label").style("fill", "white")
                        .style("font-weight", "100")
                        .style("font-size", "14px")

    d3.selectAll(".venn-area")
      .on("mouseover", function(d, i) {
        const node = d3.select(this)
        node.select("path").style("fill-opacity", .8)
                           .style("stroke-width", 3)
                           .style("stroke", "red")

        node.select(".label").style("font-weight", "100")
                           .style("font-size", "20px")
        tooltip.style("opacity", .7)
        tooltip.text(d.size + " people");
      })
      .on("mouseout", function(d, i) {
        const node = d3.select(this)
        node.select("path").style("fill-opacity", .65)
                           .style("stroke-width", 0)
        node.select("text").style("font-weight", "100")
                           .style("font-size", "18px")
        tooltip.style("opacity", 0)
      })
      .on("mousemove", function() {
        tooltip.style("left", (d3.event.pageX) + "px")
               .style("top", (d3.event.pageY - 28) + "px")
      })

    d3.selectAll(".venn-area")
      .on("click", function(d, i){
        const node = d3.select(this)
        self.props.handleUpdateTableData(self.state.allTableData, d['sets'])
        self.props.handleUpdateSetStatus(d['sets'])
        tooltip.style("opacity", 0)
      })
  }

  render() {
  	return (
      <div style={{marginLeft: 15}}>
        <g transform="translate(10, 30)" ref={node => this.node = node} />
        <p> * Left circle is always larger or equal</p>
        <RaisedButton
          label="Reset"
          style={{margin: 5}}
          onClick={this.handleReset}
          labelStyle={{fontSize: '10px',}} />
      </div>
  	)
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Venn)
