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
    if (this.props.data == null) {
      return (
        <div className="container">
          <h3>No data!</h3>
        </div>
      )
    } else {
      return (
        <div>
          <div className="col-sm-4">
            <FlexibleXYPlot
              animation
              margin={{ left: 100, right: 5, top: 20 }}
              xType="ordinal"
              stackBy="y"
              width={300}
              height={280}>
              <HorizontalGridLines />
              <YAxis
                tickFormat={v => `${v}%`}
                style={{
                  ticks: {fontSize: 14}
                }} />
              <YAxis
                hideLine
                hideTicks
                left={-80}
                title={'Percent of Population'}
                style={{
                  title: {fontSize: 14, color: '#000000'}
                }}
                top={85} />
              <XAxis
                style={{
                  ticks: {fontSize: 14}
                }}
              />
              {this.props.data.map((entry, idx) => (
                <VerticalBarSeries
                  data={entry}
                  key={idx}
                  opacity={0.8} />
              ))}
            </FlexibleXYPlot>
          </div>
          <div className="col-sm-2">
            <DiscreteColorLegend
              margin={{ left: 1, right: 1 }}
              orientation="vertical"
              items={this.props.legendItemList} />
          </div>
        </div>
      )
    }
  }
}
