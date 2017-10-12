import {
  DiscreteColorLegend,
  HorizontalGridLines,
  makeWidthFlexible,
  VerticalBarSeries,
  XAxis,
  XYPlot,
  YAxis,
} from 'react-vis'
import React from 'react'
import d3 from 'd3'

const FlexibleXYPlot = makeWidthFlexible(XYPlot)

export default class DurationBarChart extends React.Component {
  constructor(props) {
    super(props)
  }

  render() {
    return (
      <div>
        <div className="col-sm-8">
          <FlexibleXYPlot
            animation
            margin={{ left: 100, right: 30, top: 20 }}
            xType="ordinal"
            stackBy="y"
            height={250}>
            <HorizontalGridLines />
            <YAxis />
            <YAxis hideLine hideTicks left={-60} title={this.props.title} top={85} />
            <XAxis />
            {this.props.data.map((entry, idx) => (
              <VerticalBarSeries
                data={entry}
                key={idx}
                opacity={0.8} />
            ))}
          </FlexibleXYPlot>
        </div>
        <div className="col-sm-4">
          <DiscreteColorLegend
            margin={{ left: 5, right: 5 }}
            orientation="vertical"
            items={["0 day", "1 day", "2-9 days", "10-89 days", "90+ days"]} />
        </div>
      </div>
    )
  }
}
