import {
  DiscreteColorLegend,
  HorizontalGridLines,
  makeWidthFlexible,
  onValueClick,
  onItemClick,
  VerticalBarSeries,
  XAxis,
  XYPlot,
  YAxis,
} from 'react-vis'
import React from 'react'

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
            margin={{ left: 100, right: 20, top: 20 }}
            xType="ordinal"
            stackBy="y"
            width={300}
            height={270}>
            <HorizontalGridLines />
            <YAxis />
            <YAxis hideLine hideTicks left={-60} title={this.props.title} top={85} />
            <XAxis />
            {this.props.data.map((entry, idx) => (
              <VerticalBarSeries
                data={entry}
                key={idx}
                onValueClick={(datapoint, event) => {console.log(datapoint)}}
                opacity={0.8} />
            ))}
          </FlexibleXYPlot>
        </div>
        <div className="col-sm-4">
          <DiscreteColorLegend
            margin={{ left: 5, right: 1 }}
            orientation="vertical"
            onItemClick={(Object, number) => {console.log(Object)}}
            items={["0 day", "1 day", "2-9 days", "10-89 days", "90+ days"]} />
        </div>
      </div>
    )
  }
}
