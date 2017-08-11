import React from 'react'
import d3 from 'd3'
import * as venn from 'venn.js'

export default class Venn extends React.Component {
	constructor(props) {
		super(props);
	}

  componentDidMount() {
    this.createVenn()
  }

  componentDidUpdate() {
    this.createVenn()
  }

  createVenn() {
    const chart = venn.VennDiagram().width(400).height(250)
    // var tooltip = d3.select("body").select(".col-md-2").append("div")
    //                 .attr("class", "venntooltip")
    const node = this.node
    const div = d3.select(node)
    var tooltip = d3.select(node).append("div").attr("class", "venntooltip")
    div.datum(this.props.data).call(chart)
    d3.selectAll(".venn-circle path").style("fill-opacity", .5)
    d3.selectAll(".venn-area path").style("fill-opacity", .5)
    d3.selectAll("text").style("fill", "white")
                        .style("font-weight", "100")
                        .style("font-size", "18px")

    d3.selectAll(".venn-area")
      .on("mouseover", function(d, i) {
        const node = d3.select(this)
        node.select("path").style("fill-opacity", .8)
        node.select("text").style("font-weight", "100")
                           .style("font-size", "26px")
        tooltip.style("opacity", .7)
        		 	 .style("left", (d3.event.pageX) + "px")
        		 	 .style("top", (d3.event.pageY - 28) + "px");
        tooltip.text(d.size + " people");
      })
      // .on("mousemove", function() {
      //   tooltip.style("left", (d3.event.pageX) + "px")
      //          .style("top", (d3.event.pageY - 28) + "px")
      //  })
      .on("mouseout", function(d, i) {
        const node = d3.select(this)
        node.select("path").style("fill-opacity", .5)
        node.select("text").style("font-weight", "100")
                           .style("font-size", "24px")
        tooltip.style("opacity", 0)
        // const selection = d3.select(this).transition("tooltip").duration(400)
        // selection.select("path")
        //     .style("stroke-width", 0)
        //     .style("fill-opacity", d.sets.length == 1 ? .25 : .0)
        //     .style("stroke-opacity", 0);
      })
  }

  render() {
  	return (
  		<g transform="translate(10, 30)" ref={node => this.node = node} />
  	)
  }
}